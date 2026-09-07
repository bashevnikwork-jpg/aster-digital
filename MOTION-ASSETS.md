# Заміна демо на справжні роботи

Секція `#motion` («Motion у дії») зараз показує сцену, зібрану кодом: той самий екран
без анімації та з нею. Це чесна демонстрація принципу, але не ваші роботи.

Щоб поставити реальні ролики:

1. Покладіть файли у `public/assets/motion/`:
   - `landing.mp4` + `landing.webm` — запис першого екрана сайту з motion (16:10);
   - `reel.mp4` + `reel.webm` — вертикальний ролик (9:16);
   - `landing-poster.jpg`, `reel-poster.jpg` — кадри-обкладинки.
   Орієнтир: до 6 секунд, без звуку, до 2–3 МБ на файл.

2. У `parts.py`, у блоці `write("motion.html", ...)`, замініть `<div class="stage__shot">`
   і `<div class="reel__screen">` на:

   ```html
   <video class="stage__shot" autoplay muted loop playsinline
          poster="public/assets/motion/landing-poster.jpg">
     <source src="public/assets/motion/landing.webm" type="video/webm">
     <source src="public/assets/motion/landing.mp4" type="video/mp4">
   </video>
   ```

   Для «Без motion» показуйте той самий poster: перемикач знімає клас `is-motion`
   з `#motionDemo`, тож достатньо правила
   `.motion:not(.is-motion) video { display: none; }` плюс `<img>` з постером поруч.

3. Перезберіть сторінки: `python3 parts.py && python3 build.py`.
