import argparse
import yaml
import re
import sys

# Глобальный словарь для хранения констант
constants = {}

def yaml_to_custom_language(data, indent=0):
    """Преобразует структуру данных YAML в текст на учебном конфигурационном языке."""
    indent_str = " " * indent
    if isinstance(data, dict):
        entries = []
        for key, value in data.items():
            if isinstance(value, (int, float, str, list, dict)):
                entries.append(f"{indent_str} {key} => {yaml_to_custom_language(value, indent + 2)}")
            else:
                entries.append(f"{indent_str} {yaml_to_custom_language(value, indent + 2)}")
        return f"table(\n{',\n'.join(entries)}\n{indent_str})"
    elif isinstance(data, list):
        return "[ " + " ".join(yaml_to_custom_language(item, indent) for item in data) + " ]"
    elif isinstance(data, str):
        # Проверка, что строка безопасна
        if re.match(r'^[a-z][a-z0-9_]*$', data):
            return data
        elif data.startswith("//"):
            return data  # Это комментарий
        elif data.startswith("{") and data.endswith("}"):
            # Вставка константы
            const_name = data[1:-1]
            if const_name in constants:
                return str(constants[const_name])
            else:
                raise ValueError(f"Неизвестная константа: {const_name}")
        return f'@"{data}"'
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")

def validate_identifier(identifier):
    """Проверяет, что идентификатор соответствует правилам синтаксиса."""
    if not re.match(r'^[a-z][a-z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")

def parse_yaml_file(input_path):
    """Считывает и парсит YAML-файл."""
    with open(input_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

def write_output_file(output_path, content):
    """Записывает сгенерированный текст в файл."""
    with open(output_path, 'w') as file:
        file.write(content)

def parse_constants(data):
    """Извлекает константы из YAML-файла."""
    if "constants" in data:
        for key, value in data["constants"].items():
            validate_identifier(key)
            constants[key] = value

def main():
    parser = argparse.ArgumentParser(description="Инструмент для преобразования YAML в учебный конфигурационный язык.")
    parser.add_argument("--input", required=True, help="Путь к входному YAML-файлу.")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу.")

    args = parser.parse_args()

    try:
        # Чтение YAML
        data = parse_yaml_file(args.input)

        # Извлечение констант
        parse_constants(data)

        # Преобразование в учебный конфигурационный язык
        output_content = yaml_to_custom_language(data)

        # Запись в файл
        write_output_file(args.output, output_content)

        print("Трансляция завершена успешно.")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
