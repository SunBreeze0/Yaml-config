# Интсрумент преобразования YAML на учебный конфигурационный язык.

## Описание

Этот инструмент командной строки преобразует файлы YAML в текст на учебном конфигурационном языке. Поддерживается расширенный синтаксис, включая комментарии, массивы, словари, константы и их вычисление.

### Основные возможности
- **Комментарии**: Вставка однострочных комментариев.
- **Массивы**: Поддержка массивов формата `[ значение значение ... ]`.
- **Словари**: Поддержка словарей формата `table( имя => значение, ...)`.
- **Константы**: Объявление констант с помощью секции `constants` в YAML.
- **Использование констант**: Ссылки на константы через `{имя}` в основных данных YAML.
- **Строки**: Поддержка строк формата `@"Это строка"`.
- **Синтаксическая проверка**: Проверяет корректность идентификаторов и выявляет ошибки.

## Установка

Скопируйте репозиторий и убедитесь, что установлен Python версии 3.8 или выше.

```bash
pip install pyyaml
```

## Использование

### Синтаксис

```bash
python yaml_to_config_extended.py --input <входной файл YAML> --output <выходной файл>
```

### Пример

#### Входной YAML:
```yaml
constants:
  server_name: "example_server"
  max_connections: 500

server:
  name: "{server_name}"
  max_connections: "{max_connections}"
  metrics: [ cpu, memory, disk ]
```

#### Выходной файл:
```plaintext
def server_name = @"example_server";
def max_connections = 500;

table(
  server => table(
    name => server_name,
    max_connections => max_connections,
    metrics => [ cpu memory disk ]
  )
)
```

## Подробности синтаксиса

### Комментарии
Комментарии обозначаются двойным слешем (`//`) и игнорируются при обработке.
```yaml
// Это комментарий
```

### Константы
Константы задаются в секции `constants` и могут быть использованы через `{имя}`.
```yaml
constants:
  my_const: 42
value: "{my_const}"
```

### Массивы
```yaml
array:
  - value1
  - value2
```
преобразуется в:
```plaintext
[ value1 value2 ]
```

### Словари
```yaml
dictionary:
  key1: value1
  key2: value2
```
преобразуется в:
```plaintext
table(
  key1 => value1,
  key2 => value2
)
```

### Строки
Строки оборачиваются в `@"строка"`, если содержат символы, не подходящие под идентификаторы.

### Обработка ошибок
Инструмент проверяет корректность:
- Идентификаторов (должны соответствовать `[a-z][a-z0-9_]*`).
- Ссылок на константы.

Если обнаруживается ошибка, программа завершает работу с сообщением.
