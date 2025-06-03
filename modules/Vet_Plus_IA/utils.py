import os

def save_list_to_txt(content, filename):
    # Define the log directory path
    # log_dir = "./log/"

    # Create the log directory if it doesn't exist
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    #     print(f"Created directory: {log_dir}")

    # Full path to the file
    # file_path = os.path.join(log_dir, filename)
    file_path = filename

    # Check if file exists
    file_exists = os.path.isfile(file_path)

    # Open file in appropriate mode
    mode = 'a' if file_exists else 'w'
    with open(file_path, mode) as file:
        # Add newline if appending to existing file with content
        if file_exists and os.path.getsize(file_path) > 0:
            file.write("\n")

        # Write list items
        file.write(f"{content}\n")

    # if file_exists:
    #     print(f"List appended to existing file {file_path}")
    # else:
    #     print(f"New file {file_path} created with list data")

def read_file_to_vector(filename):
    vector = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                vector.append(line.rstrip('\n'))
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
    except UnicodeDecodeError as e:
        print(f"Erro de decodificação ao ler o arquivo '{filename}' com a codificação '{encoding}': {e}")
        print("Tente abrir o arquivo com uma codificação diferente (ex: 'latin-1', 'cp1252').")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo '{filename}': {e}")
    return vector

