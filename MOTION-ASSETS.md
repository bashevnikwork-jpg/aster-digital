# Медіа для секції Motion і портфоліо

## Що вже стоїть

- `public/assets/motion/logo-reveal.mp4` — анімація логотипа (H.264/AAC, 1.2 МБ).
  Вставлена на головній у секції `#motion` як `autoplay muted loop playsinline`.

## Що варто додати

1. **Постер для відео.** Зараз до першого кадру видно чорний прямокутник.
   Покладіть кадр у `public/assets/motion/logo-reveal-poster.jpg` і додайте
   `poster="public/assets/motion/logo-reveal-poster.jpg"` до `<video>` у `parts.py`.

2. **WebM-версія** для ширшої підтримки й меншої ваги:
   ```
   ffmpeg -i logo-reveal.mp4 -c:v libvpx-vp9 -crf 34 -b:v 0 -an logo-reveal.webm
   ```
   Далі замініть `src` на два `<source>`: спочатку WebM, потім MP4.

3. **Вертикальні ролики** (Reels, product-анімації). Формат 9:16, до 6 секунд,
   без звуку, 2–3 МБ. Під них у секції вже є місце — блок `.reel__phone`
   міняється на `<video>` за тим самим принципом.

4. **Скриншот Ashad Barbershop.** Картка в портфоліо поки що показує тёмну
   плитку з посиланням на живий сайт, бо знімок зробити не вдалося.
   Покладіть `public/assets/screenshots/ashad.webp` (16:10) і приберіть
   `'ashad'` зі словника `LIVE` у `parts.py` — картка стане як інші.

Після будь-якої зміни: `python3 parts.py && python3 build.py`.
