@csrf_exempt
@require_POST
def webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    '''who_time = timezone.now().strftime("%d %B %Y, %H:%M")
    r, _ = Results.objects.get_or_create(who='crm')
    r.json_data = data
    r.who_desc = who_time
    r.save()'''
    dict_data = bid(data)


def personal_kurier(request, now, context, st_pk):
    # кабинет курьера с шаблоном family_kurier
    # st_pk - строковый аргумент
    # st_pk - 0: когда мес период не введен или нач запуск
    # st_pk - month, year, ss_pk - дата периода и pk периода Statistics_service

    person = request.user
    M = Managers.objects.get(family__pk=person.pk)

    formK = StatsDescrForm() # передаем в шаблон форму для созд/ред строкового
    # периода (00.00 - 00.00)
    context['formK'] = formK
    context['description'] = '00.00 - 00.00'

    date_for_stats = now
    ss_pk = 0 # ss_pk = 0 нет, не выбрана/не создана группа Statistics_service
    week_count = 1 # по умолчанию 1 неделя

    month, year = now.strftime("%m"), now.strftime("%Y")
    month_before = int(month) - 1
    year_before = year
    if int(month) - 1 == 0:
        month_before, year_before = 12, int(year) - 1
    if month_before < 10:
        month_before = f'0{month_before}'

    form = KurierFormWeek() # курьер вносит н. заявки, сумму з., дату
    context['form_st'] = form

    if request.method == 'POST':
        form = KurierFormWeek(request.POST)
        if form.is_valid():
            if st_pk != 0:
                m_y = re.split(':',st_pk)
                if len(m_y) == 2:
                    month, year = m_y[0].strip(), m_y[1].strip() # для опред даты под стат
                if len(m_y) == 3:
                    month, year, ss_pk = m_y[0].strip(), m_y[1].strip(), m_y[2].strip()

            bids = form.cleaned_data['bids']
            summa = form.cleaned_data['summa']
            date_field = form.cleaned_data['date_field']

            try:
                ss = Statistics_service.objects.get(pk=int(ss_pk))
                week_count = ss.week_count
            except:
                week_count = 1
                kuriers = Managers.objects.filter(family__groups__name='kurier_group')
                kurier = kuriers.first() if kuriers.exists() else None
                service_ = Service.objects.filter(kind='Курьер', sloznostPK='простой')
                kurier_serv = service_.first() if service_.exists() else None

                st = Statistics_service.objects.filter(managers=kurier,
                service=kurier_serv,
                week_count=1, date__month=month, date__year=year)

                if st.exists():
                    ss = st.first()
                else:
                    new_now = now.replace(year=int(year), month=int(month))
                    ss = Statistics_service.objects.create(managers=kurier,
                    service=kurier_serv,
                    week_count=1, date=new_now)
                #kurier_periods(request, st_pk, 1)

            #year, month, day = date_field.split('-')
            #new_now = now.replace(year=int(year), month=int(month), day=int(day))

            try:
                bidskur = BidsKurier.objects.create(ID=bids, kurier_summa=summa,
                date_ch=date_field, kurier_period=ss)
                messages.warning(
                request,
                f'Добавлена заявка: {bids}, сумма: {summa}, дата: {date_field},\
                 неделя: {week_count}')
            except Exception as e:
                messages.warning(request,f'Заявка {bids} уже существует')

    st_period = set([x.date.strftime("%m: %Y") for x in\
    Statistics_service.objects.filter(managers=M)])
    st_period.add(f"{month}: {year}")
    st_period.add(f"{month_before}: {year_before}")
    date_tuples = [
    (int(date.split(': ')[0]), int(date.split(': ')[1])) for date in st_period
                    ]
    sorted_dates = sorted(date_tuples, key=lambda x: (x[1], x[0]))
    sorted_dates_str = [f'{x}:{y}' for x, y in sorted_dates]

    context['st_period'] = sorted_dates_str # набор отсорт-ых мес периодов
    if st_pk != 0:
        m_y = re.split(':',st_pk)
        try:
            month, year = m_y[0].strip(), m_y[1].strip()
        except:
            month, year = now.strftime("%m"), now.strftime("%Y")
        if len(m_y) == 3:
            ss_pk = m_y[2].strip()
            name_ss = Statistics_service.objects.get(pk=int(ss_pk))
            week_count = name_ss.week_count
            messages.success(request,
            f'Период (нед): {name_ss.description}, {week_count}неделя')
            context['description'] = name_ss.description

        messages.success(request,f'Период (мес):{st_pk}')
    else:
        #now = timezone.now()
        month, year = now.strftime("%m"), now.strftime("%Y")
        messages.warning(request,f'Период3:{month}:{year}')

    sal = Salary(month, year) # класс ЗП в том числе и курьера в salary.py
    context['manager_stats_per_period'] = sal.salary_kurier(plan_stavka_=True,
    no_stavka=False, week=week_count)


    context['st_pk'] = [] #must be clear!
    context['bids_per_period'] = [] #must be clear!
    context['ss_pk'] = ss_pk
    context['week_count'] = {week_count: '#ffebcd'}


    return context


def kurier_del(request, kb_pk):
    # для удаления в шаблоне family_kurier выбранного BidsKurier

    bidskur = BidsKurier.objects.get(pk=kb_pk)
    st_pk = bidskur.date_ch.strftime("%m: %Y")
    bidskur.delete()

    messages.warning(request,f'Удалена заявка: {bidskur.ID}')

    return  HttpResponseRedirect(
                                reverse('family',
                                kwargs={'st_pk':st_pk}
                                )
                                )


def kurier_periods(request,st_pk, ss_pk):
    # работаем с Statistics_service для обьединения в группы
    #  с BidsKurier (заявки курьера)
    # со старта st_pk = month, year (группа Statistics_service за период не создана)
    # в конце возвращаем для 'family' с аргументом st_pk включающем st_.pk созд-ой группы
    # для GET запроса из family_kurier (кур шаблона) ss_pk - номер недели (1-5)
    # для POST запроса создаем/редактирем строковый период (00.00 - 00.00) для выбранного
    # периода Statistics_service, где ss_pk уже, !!!внимание, pk периода Statistics_service

    now = timezone.now()

    m_y = re.split(':',st_pk)
    try:
        month, year = m_y[0].strip(), m_y[1].strip()
    except:
        messages.warning(
        request,f'Ошибка при переходе в: {month}-{year}:')
        return  HttpResponseRedirect(
                                    reverse('family',
                                    kwargs={'st_pk':st_pk}
                                    )
                                    )
        #month, year = now.strftime("%m"), now.strftime("%Y")

    kuriers = Managers.objects.filter(family__groups__name='kurier_group')
    kurier = kuriers.first() if kuriers.exists() else None
    service_ = Service.objects.filter(kind='Курьер', sloznostPK='простой')
    kurier_serv = service_.first() if service_.exists() else None

    if request.method == 'GET':
        # находим период (с номером редели) Statistics_service
        st = Statistics_service.objects.filter(managers=kurier, service=kurier_serv,
        week_count=ss_pk, date__month=month, date__year=year)

        if st.exists():
            st_ = st.first()
        else:
            # если не находим - создаем
            new_now = now.replace(year=int(year), month=int(month))
            st_ = Statistics_service.objects.create(managers=kurier, service=kurier_serv,
            week_count=ss_pk, date=new_now)

    if request.method == 'POST':
        # создаем/редактирем строковый период (00.00 - 00.00)
        form = StatsDescrForm(request.POST)
        if form.is_valid():
            descr_period = request.POST['description']

            try:
                st_ = Statistics_service.objects.get(pk=ss_pk)
            except:
                # когда выбираем период без недель, ставим 1 неделю
                # replace по сути для выделения из now year и month
                # year и month от переданного периода в качестве аргумента дан фун-ии
                new_now = now.replace(year=int(year), month=int(month))
                st_ = Statistics_service.objects.create(managers=kurier,
                service=kurier_serv,
                week_count=1, date=new_now)

            st_.description = descr_period
            st_.save()

            messages.warning(
            request,f'Задан период: {st_.description}')

    st_pk += f': {st_.pk}'
    return  HttpResponseRedirect(
                                reverse('family',
                                kwargs={'st_pk':st_pk}
                                )
                                )
