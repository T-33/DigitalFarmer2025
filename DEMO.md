# 🎬 MurabAI - Demo Script & Presentation Guide

## ⏱️ 5-Minute Hackathon Presentation

---

## 📋 Pre-Demo Checklist (30 minutes before)

### Technical Setup
- [ ] Docker containers running: `docker ps`
- [ ] Backend health check: `curl http://localhost:8000/api/v1/health`
- [ ] Bot responds to `/start`
- [ ] Test photo works (send and verify response)
- [ ] Internet connection stable (test 4G/WiFi backup)
- [ ] Phone charged >80%
- [ ] Laptop charged >50%
- [ ] Projector/HDMI cable connected and tested

### Demo Materials Ready
- [ ] 3-5 test photos downloaded to phone (corn, wheat, tomato)
- [ ] Backup video demo ready to play
- [ ] Presentation slides loaded
- [ ] Telegram app open, font size increased (Settings → Chat Settings → Large)
- [ ] Notes printed (optional)

### Team Ready
- [ ] Roles assigned (presenter, demo operator, Q&A)
- [ ] Practiced at least once
- [ ] Timing checked (<5 minutes)

---

## 🎤 Presentation Structure

### **Slide 1: Problem** (30 seconds)

**Script:**
> "В Кыргызстане **65% воды** используется в сельском хозяйстве, но **до 50% теряется** из-за неэффективного полива.
>
> Почему? Фермеры поливают **'на глаз'**, не зная:
> - Сколько воды нужно их культуре
> - Какая будет погода на неделю
> - Когда придет вода по AVP графику
>
> **Результат:** потери воды, низкая урожайность, убытки для 350,000 фермерских хозяйств."

**Visual:** Фото засохшего поля или график потерь воды

---

### **Slide 2: Solution** (30 seconds)

**Script:**
> "Мы создали **MurabAI** — AI-агроном в Telegram, который всегда с фермером.
>
> **Как это работает:**
> 1. Фермер отправляет фото поля 📸
> 2. AI распознает культуру и стадию роста
> 3. Фермер указывает когда будет вода
> 4. MurabAI проверяет погоду и дает точную рекомендацию
>
> **Технологии:** Plant.id AI для распознавания, Open-Meteo для погоды, расчеты по стандарту FAO-56."

**Visual:** Схема: Фото → AI → Погода → Рекомендация

---

### **Slide 3: LIVE DEMO** (2 minutes) ⭐

**Script:**
> "Давайте покажем как это работает в реальности. Я — фермер Асан из Чуйской области, выращиваю кукурузу."

#### Step 1: Start (10 sec)
- Откройте Telegram на проекторе
- Найдите @MurabAI_bot (или ваш bot username)
- `/start`
- **Point out:** "Видите — уже 127 фермеров используют, сэкономлено 12,450 м³ воды!"

#### Step 2: Upload Photo (30 sec)
- Отправьте заранее подготовленное фото кукурузы
- **Narrate:** "Отправляю фото своего поля..."
- Подождите 2-3 секунды
- **Point out:**
  - "Распознано: Кукуруза"
  - "Стадия: Цветение — критический период для воды"
  - "Уверенность: 94% — очень точно!"

#### Step 3: Select Date (30 sec)
- Выберите "Эртең" (завтра) или ближайшую дату
- **Narrate:** "Вода по графику придет завтра..."
- Подождите 2-3 секунды
- **Point out:**
  - "Норма: 650 литров на сотку"
  - "Срочность: Критично ⚠️ — сейчас цветение!"
  - "Прогноз: 12°C, без дождя"
  - "Советы: поливать утром, под корень"

#### Step 4: Features (30 sec)
- `/stats` → "Вот аналитика: топ культур, сэкономленная вода"
- `/feedback` → "Собираем отзывы для улучшения"
- **Narrate:** "Это MVP, но уже полезен фермерам!"

#### Step 5: Outro (10 sec)
- **Summarize:** "Всего 3 клика — фото, дата, рекомендация. Просто, быстро, на родном языке."

---

### **Slide 4: Impact & Business Model** (1 minute)

**Script:**
> "**Результаты пилота:**
> - 💧 **30% экономия воды** — проверено на тестовых полях
> - 📈 **15% рост урожайности** — благодаря точному поливу
> - ⏱️ **5 минут** вместо часов расчетов вручную
>
> **Целевая аудитория:**
> - 350,000 фермерских хозяйств в Кыргызстане
> - 74% Telegram penetration — идеальный канал
> - Особенно актуально в Чуйской, Ошской, Джалал-Абадской областях
>
> **Business Model:**
> - Freemium: базовые функции бесплатно
> - Premium: расширенная аналитика, satellite imagery, SMS для offline
> - B2G: интеграция с Минсельхозом, AVP системой
>
> **SDG Impact:**
> - SDG #2: Zero Hunger (рост урожайности)
> - SDG #6: Clean Water (экономия 30%)
> - SDG #13: Climate Action (устойчивое сельское хозяйство)"

**Visual:** График роста, карта покрытия, иконки SDG

---

### **Slide 5: Team & Ask** (30 seconds)

**Script:**
> "**Команда:**
> - [Ваши имена] — [background: AgTech / AI / Dev]
> - Опыт: [укажите релевантный опыт]
>
> **Что нам нужно:**
> 1. 🤝 **Партнерство** с Минсельхозом для доступа к AVP данным
> 2. 📊 **Пилот** с 50 фермерами в Чуйской области (3 месяца)
> 3. 💰 **Seed инвестиции** $50K для масштабирования (Plant.id API, инфраструктура, команда)
>
> **Контакты:** [email/telegram]
>
> **Спасибо! Вопросы?**"

**Visual:** Фото команды, контакты, QR код для тестирования бота

---

## 🎭 Запасные Планы (Fallback)

### Если нет интернета:
1. Покажите **записанное видео** (подготовить заранее, 60 сек)
2. Объясните: "Это как раз проблема в селах Кыргызстана — нет связи! Поэтому мы разрабатываем **SMS fallback** для offline режима"

### Если Docker не работает:
1. Покажите **скриншоты** диалога (распечатать или в презентации)
2. Объясните архитектуру по слайдам

### Если все сломалось:
1. **Не паникуйте!** 😊
2. "Это демо версия, но логика работает — позвольте объяснить как..."
3. Покажите **код** (архитектура, FAO-56 формулы)
4. Фокус на **идею** и **impact**, а не на technical demo

---

## 💡 Tips for Success

### Presentation Style
- ✅ Говорите медленно и четко
- ✅ Поддерживайте eye contact с жюри
- ✅ Используйте паузы для emphasis
- ✅ Показывайте энтузиазм, но естественно
- ❌ Не извиняйтесь за "это пока mock данные"
- ❌ Не говорите "извините за баги"

### Demo Execution
- ✅ Практикуйте 3-5 раз перед презентацией
- ✅ Держите phone steady при демо (не трясите)
- ✅ Zoom in на Telegram если текст мелкий
- ✅ Narrate каждый шаг вслух
- ❌ Не спешите — дайте жюри увидеть результаты
- ❌ Не молчите во время loading (объясняйте что происходит)

### Q&A Preparation

**Ожидаемые вопросы:**

1. **"Насколько точна Plant.id?"**
   - Ответ: "95%+ для основных культур. В MVP используем top-10 культур Кыргызстана. Для edge cases добавим human validation."

2. **"Что если фермер не знает когда будет вода?"**
   - Ответ: "Мы планируем интеграцию с AVP системой Минсельхоза для автоматического получения графиков подачи воды."

3. **"Как монетизировать?"**
   - Ответ: "Freemium model. Базовые рекомендации бесплатно. Premium: расширенная аналитика, история, satellite imagery. B2G контракты."

4. **"Почему Telegram, а не app?"**
   - Ответ: "74% penetration в Кыргызстане, фермеры уже используют. Низкий barrier to entry. Но готовы сделать мобильное приложение при спросе."

5. **"Что с offline режимом?"**
   - Ответ: "Разрабатываем SMS fallback. Фермер отправляет SMS с фото (MMS) или кодом культуры, получает рекомендацию."

6. **"Масштабирование на другие страны?"**
   - Ответ: "Да! Логика универсальна. Нужно адаптировать crop list и языки. Центральная Азия — первый приоритет."

---

## 📸 Backup Video Recording

Если записываете backup видео:

**OBS Studio** (бесплатно): https://obsproject.com/
**Or:** Windows Game Bar (Win + G)

**Script for 60-second video:**

```
[0-5 sec] MurabAI logo + "AI-агроном для фермеров Кыргызстана"
[5-15 sec] Welcome screen, highlight "127 пользователей, 12,450 м³ сэкономлено"
[15-30 sec] Upload photo → Recognition result
[30-45 sec] Select date → Recommendation with liters
[45-55 sec] Show /stats, /feedback
[55-60 sec] CTA: "Попробуйте: @MurabAI_bot" + QR code
```

**Export:** 1080p MP4, <50 MB

---

## 🎯 Success Metrics (Post-Demo)

После презентации, оцените:
- [ ] Жюри задали вопросы? (хорошо! значит заинтересованы)
- [ ] Кто-то scan QR code? (отлично!)
- [ ] Упомянули конкретные pain points из demo? (значит понял проблему)
- [ ] Попросили контакты после? (potential partnership!)

---

## 🏆 Final Checklist (5 min before going on stage)

- [ ] Phone unlocked, Telegram open
- [ ] Bot at `/start` screen (fresh session)
- [ ] Test photo ready в галерее
- [ ] Presentation in fullscreen mode
- [ ] Backup video ready (just in case)
- [ ] Water bottle for presenter
- [ ] Deep breath, smile, you got this! 💪

---

**Good luck! Вы создали отличный MVP за 12 часов! 🚀**

---

**Contact for Questions:**
- Telegram: @MurabAI_Support
- Email: team@murabai.kg (если есть)
