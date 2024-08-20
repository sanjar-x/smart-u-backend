# Changelog

Все заметные изменения в этом проекте будут задокументированы в этом файле.

Формат этого файла основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/), и этот проект следует [Semantic Versioning](https://semver.org/lang/ru/) (Семантическому Версионированию).

## [Unreleased]
### Добавлено
- Запуск `detector engine` с динамическими аргументами, что позволяет гибко конфигурировать работу движка в зависимости от текущих условий и потребностей.
- Добавлена обработка `detection quality` и `Liveness` в `detector engine`. Эта функциональность позволяет оценивать качество детекций и проверять наличие признаков живости на изображениях, что повышает надежность и точность системы.
- Добавлена конфигурация камер, что позволяет настраивать параметры камер для оптимизации детекций и улучшения качества видеоанализа.
- Добавлен трекинг лиц по территории, что позволяет отслеживать перемещения лиц в режиме реального времени на всей охраняемой территории, улучшая безопасность и возможности мониторинга.
- Добавлена поддержка Redis `pipeline()` для выполнения групп команд, что позволяет значительно сократить сетевые задержки и улучшить производительность при выполнении множества команд Redis одновременно.
- Добавлен динамический Git pool, что позволяет более эффективно управлять параллельными задачами и уменьшает задержки при выполнении операций с Git, особенно в условиях многопользовательской среды или CI/CD систем.
- Добавлен динамический build для `detector engine`, что позволяет компилировать и собирать компоненты движка на основе текущих условий и требований, улучшая гибкость и адаптируемость системы.
- Добавлена валидация для проверки уже добавленного лица

### Изменено
- Метод `_setattr_instance` в классе `Base` был заменен на вызов `session.refresh`. Это изменение направлено на обеспечение более надежного обновления атрибутов объекта, синхронизируя их с актуальными данными из базы данных.

    <!-- ret = await handler(*args)
  File "/home/ocean/Desktop/smart-u-backend/app/connections/socketio.py", line 49, in connect
    await slot.get_active(session)
  File "/home/ocean/Desktop/smart-u-backend/app/core/models.py", line 821, in get_active
    await self.get_where(
  File "/home/ocean/Desktop/smart-u-backend/app/core/models.py", line 156, in get_where
    obj = result.scalar_one_or_none()
  File "/home/ocean/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 1487, in scalar_one_or_none
    return self._only_one_row(
  File "/home/ocean/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 805, in _only_one_row
    raise exc.MultipleResultsFound(
<!-- sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when one or none was required --> 
