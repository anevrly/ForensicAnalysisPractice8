import hashlib
import time
import itertools

def generate_md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def dictionary_with_suffix_attack(target_hash, dictionary_file, max_suffix_length=3):
    start_time = time.time()
    try:
        with open(dictionary_file, 'r', encoding='latin1') as file:
            for line in file:
                base_word = line.strip()
                
                if generate_md5_hash(base_word) == target_hash:
                    elapsed_time = time.time() - start_time
                    return base_word, elapsed_time

                for suffix_length in range(1, max_suffix_length + 1):
                    for suffix in itertools.product("0123456789", repeat=suffix_length):
                        word = base_word + ''.join(suffix)
                        if generate_md5_hash(word) == target_hash:
                            elapsed_time = time.time() - start_time
                            return word, elapsed_time

    except FileNotFoundError:
        print(f"Slovníkový soubor {dictionary_file} nebyl nalezen.")
        return None, None
    except UnicodeDecodeError as e:
        print(f"Chyba při dekódování: {e}")
        return None, None
    return None, None


if __name__ == "__main__":
    target_hash = "puthashere"

    dictionary_file = "rockyou.txt"

    print(f"Prolamování hashe: {target_hash}")
    print(f"Použití slovníkového souboru: {dictionary_file}")

    result, elapsed_time = dictionary_with_suffix_attack(target_hash, dictionary_file)

    if result:
        print(f"Heslo bylo prolomeno: {result}")
        print(f"Doba prolomení: {elapsed_time:.2f} sekund")
    else:
        print("Heslo nebylo nalezeno")
