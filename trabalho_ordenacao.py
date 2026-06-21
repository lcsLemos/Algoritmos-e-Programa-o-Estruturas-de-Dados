import time
import random
import sys
import statistics
import copy

sys.setrecursionlimit(200000)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]: largest = l
        if r < n and arr[largest] < arr[r]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    def _quick_sort(items, low, high):
        if low < high:
            pi = partition(items, low, high)
            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)

    def partition(items, low, high):
        mid = (low + high) // 2
        items[mid], items[high] = items[high], items[mid]
        pivot = items[high]
        i = low - 1
        for j in range(low, high):
            if items[j] <= pivot:
                i = i + 1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)

def gerar_cenarios(n):
    return {
        "Crescente sem repetidos": list(range(n)),
        "Decrescente sem repetidos": list(range(n, 0, -1)),
        "Aleatório sem repetidos": random.sample(range(n * 10), n),
        "Aleatório com repetidos": [random.randint(0, n // 2) for _ in range(n)]
    }

def medir_tempo(algoritmo, array_original):
    tempos = []
    for _ in range(10):
        arr_teste = copy.deepcopy(array_original)
        
        inicio = time.perf_counter_ns()
        algoritmo(arr_teste)
        fim = time.perf_counter_ns()
        
        tempos.append(fim - inicio)
    
    media = statistics.mean(tempos)
    if len(tempos) > 1:
        desvio_padrao = statistics.stdev(tempos)
    else:
        desvio_padrao = 0

    limite_inferior = media - desvio_padrao
    limite_superior = media + desvio_padrao
    tempos_validos = [t for t in tempos if limite_inferior <= t <= limite_superior]
    
    media_final = sum(tempos_validos) / len(tempos_validos) if tempos_validos else media
    return int(media_final)

if __name__ == "__main__":
    tamanhos_array = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
    
    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Heap Sort": heap_sort,
        "Shell Sort": shell_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }
    
    nomes_cenarios = [
        "Crescente sem repetidos", 
        "Decrescente sem repetidos", 
        "Aleatório sem repetidos", 
        "Aleatório com repetidos"
    ]
    
    resultados = {cenario: {alg: [] for alg in algoritmos} for cenario in nomes_cenarios}

    print("Iniciando testes.")
    
    for n in tamanhos_array:
        print(f"\nTestando array de tamanho {n}...")
        cenarios = gerar_cenarios(n)
        
        for nome_cenario, array_base in cenarios.items():
            for nome_algoritmo, func_algoritmo in algoritmos.items():
                tempo_calculado = medir_tempo(func_algoritmo, array_base)
                resultados[nome_cenario][nome_algoritmo].append(str(tempo_calculado))
    
    with open("resultados.md", "w", encoding="utf-8") as f:
        f.write("Análise Comparativa dos Métodos de Ordenação\n\n")
        f.write("Tempos computados em **nanossegundos**. Média final gerada a partir de 10 execuções filtrando os valores através do cálculo de desvio padrão.\n\n")
        
        for cenario in nomes_cenarios:
            f.write(f"Cenário: {cenario}\n")
            f.write("| Tamanho do Array (n) | Bubble Sort | Insertion Sort | Selection Sort | Heap Sort | Shell Sort | Merge Sort | Quick Sort |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            
            for i, n in enumerate(tamanhos_array):
                linha = f"| {n} | "
                tempos_linha = [resultados[cenario][alg][i] for alg in algoritmos.keys()]
                linha += " | ".join(tempos_linha) + " |\n"
                f.write(linha)
            f.write("\n")
          
            
    print("\nTestes concluídos!")
