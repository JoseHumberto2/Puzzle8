import tkinter as tk  
from tkinter import messagebox  
import heapq  
from typing import List, Tuple, Optional 

# ========== CLASE ESTADOPUZZLE8 ==========
class EstadoPuzzle8:
    def __init__(self, tablero: List[int], padre=None, movimiento="", profundidad=0):
        self.tablero = tablero[:]  
        self.padre = padre   
        self.movimiento = movimiento  
        self.profundidad = profundidad  # g(n) - costo real desde el inicio
        self.pos_vacia = self.tablero.index(0)  
    
    def __eq__(self, otro):
        return self.tablero == otro.tablero
    
    def __hash__(self):
        return hash(tuple(self.tablero))
    
    # IMPLEMENTACIÓN DE A*: Función de evaluación f(n) = g(n) + h(n)
    def __lt__(self, otro):
        """
        - g(n): profundidad (costo real desde el inicio)
        - h(n): heurística Manhattan
        """
        return (self.profundidad + self.heuristica()) < (otro.profundidad + otro.heuristica())
    
    # heurística Manhattan
    def heuristica(self) -> int:
        distancia = 0
        for i in range(9):
            if self.tablero[i] != 0:  # Ignoramos el espacio vacío
                # Posición actual de la pieza
                fila_actual, col_actual = i // 3, i % 3

                fila_obj, col_obj = (self.tablero[i] - 1) // 3, (self.tablero[i] - 1) % 3
                # FÓRMULA MANHATTAN: |x1-x2| + |y1-y2|
                distancia += abs(fila_actual - fila_obj) + abs(col_actual - col_obj)
        return distancia
    
    def es_objetivo(self) -> bool:
        return self.tablero == [1, 2, 3, 4, 5, 6, 7, 8, 0] # estado objetivo
    
    def obtener_movimientos_posibles(self) -> List[str]:
        movimientos = []
        fila, col = self.pos_vacia // 3, self.pos_vacia % 3
        if fila > 0: movimientos.append("ARRIBA")
        if fila < 2: movimientos.append("ABAJO")
        if col > 0: movimientos.append("IZQUIERDA")
        if col < 2: movimientos.append("DERECHA")
        return movimientos
    
    def realizar_movimiento(self, direccion: str) -> Optional['EstadoPuzzle8']:
        """Genera un nuevo estado aplicando un movimiento"""
        if direccion not in self.obtener_movimientos_posibles():
            return None
        nuevo_tablero = self.tablero[:]
        pos_vacia = self.pos_vacia  

        if direccion == "ARRIBA": nueva_pos = pos_vacia - 3
        elif direccion == "ABAJO": nueva_pos = pos_vacia + 3
        elif direccion == "IZQUIERDA": nueva_pos = pos_vacia - 1
        else: nueva_pos = pos_vacia + 1
        
        # Intercambia la pieza con el espacio vacío
        nuevo_tablero[pos_vacia], nuevo_tablero[nueva_pos] = nuevo_tablero[nueva_pos], nuevo_tablero[pos_vacia]
        return EstadoPuzzle8(nuevo_tablero, self, direccion, self.profundidad + 1)

# ========== CLASE SOLUCIONADORPUZZLE8 ==========
class SolucionadorPuzzle8:
    def resolver(self, estado_inicial: EstadoPuzzle8) -> Tuple[List[str], int]:
        if estado_inicial.es_objetivo():
            return [], 0
        
        abiertos = [estado_inicial]
        cerrados = set()
        explorados = 0

        while abiertos:
            # A*: Selecciona el nodo con menor f(n) = g(n) + h(n)
            estado_actual = heapq.heappop(abiertos)
            
            if estado_actual in cerrados:
                continue
                
            cerrados.add(estado_actual)
            explorados += 1
            
            # Verifica si llegamos al objetivo
            if estado_actual.es_objetivo():
                return self._reconstruir_camino(estado_actual), explorados
            
            for mov in estado_actual.obtener_movimientos_posibles():
                siguiente = estado_actual.realizar_movimiento(mov)
                if siguiente and siguiente not in cerrados:
                    heapq.heappush(abiertos, siguiente)

        return [], explorados
    
    def _reconstruir_camino(self, estado: EstadoPuzzle8) -> List[str]:
        """Reconstruye la secuencia de movimientos desde el nodo objetivo hasta el inicial"""
        camino = []
        while estado.padre:
            camino.append(estado.movimiento)
            estado = estado.padre
        return camino[::-1]  # Invierte para obtener el orden correcto

# ======== CLASE INTERFAZPUZZLE8 ==========
class InterfazPuzzle8:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Puzzle 8 - Resolución Automática")
        self.ventana.geometry("400x530")
        self.ventana.configure(bg="#2c3e50")
        self.solucionador = SolucionadorPuzzle8()
        self.movimientos_solucion = []
        self.indice_mov = 0
        self.tablero_fijo = [5, 2, 4, 3, 0, 1, 7, 8, 6] # estado inicial
        self.estado_actual = EstadoPuzzle8(self.tablero_fijo)
        self.crear_interfaz()
        self.actualizar_tablero()
    
    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="PUZZLE 8",
            font=("Arial", 24, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        titulo.pack(pady=20)
        
        self.marco_tablero = tk.Frame(self.ventana, bg="#34495e", relief="raised", bd=3)
        self.marco_tablero.pack(pady=20)
        
        self.botones = []
        for i in range(3):
            fila = []
            for j in range(3):
                btn = tk.Button(
                    self.marco_tablero,
                    text="",
                    font=("Arial", 18, "bold"),
                    width=4,
                    height=2,
                    bg="#3498db",
                    fg="white",
                    relief="raised",
                    bd=2,
                    state="disabled"
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                fila.append(btn)
            self.botones.append(fila)
        
        marco_controles = tk.Frame(self.ventana, bg="#2c3e50")
        marco_controles.pack(pady=20)
        
        estilo_btn = {
            "font": ("Arial", 12, "bold"),
            "bg": "#27ae60",
            "fg": "white",
            "activebackground": "#2ecc71",
            "relief": "raised",
            "bd": 2,
            "padx": 15,
            "pady": 5
        }
        
        tk.Button(marco_controles, text="Resolver", command=self.resolver_puzzle, **estilo_btn).pack(side="left", padx=5)
        tk.Button(marco_controles, text="Siguiente Paso", command=self.siguiente_paso_solucion, **estilo_btn).pack(side="left", padx=5)        

        self.etiqueta_info = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#2c3e50",
            wraplength=350
        )
        self.etiqueta_info.pack(pady=10)
    
    def actualizar_tablero(self):
        for i in range(3):
            for j in range(3):
                pos = i * 3 + j
                valor = self.estado_actual.tablero[pos]
                if valor == 0:
                    self.botones[i][j].config(text="", bg="#2c3e50", state="disabled")
                else:
                    self.botones[i][j].config(text=str(valor), bg="#3498db", state="disabled")
    
    def resolver_puzzle(self):
        if self.estado_actual.es_objetivo():
            self.etiqueta_info.config(text="El puzzle ya está resuelto.")
            return
        self.etiqueta_info.config(text="Resolviendo puzzle... espera...")
        self.ventana.update()
        
        copia = EstadoPuzzle8(self.estado_actual.tablero)
        solucion, explorados = self.solucionador.resolver(copia)
        
        if solucion:
            self.movimientos_solucion = solucion
            self.indice_mov = 0
            self.etiqueta_info.config(
                text=f"Solución encontrada: {len(solucion)} movimientos, {explorados} estados explorados."
            )
        else:
            self.etiqueta_info.config(text="No se pudo encontrar una solución.")
    
    def siguiente_paso_solucion(self):
        if not self.movimientos_solucion:
            self.etiqueta_info.config(text="Hacer clic en Resolver.")
            return
            
        if self.indice_mov >= len(self.movimientos_solucion):
            self.etiqueta_info.config(text="No hay más pasos en la solución.")
            return
        
        mov = self.movimientos_solucion[self.indice_mov]
        nuevo = self.estado_actual.realizar_movimiento(mov)
        
        if nuevo:
            self.estado_actual = nuevo
            self.indice_mov += 1
            self.actualizar_tablero()
            
            if self.estado_actual.es_objetivo():
                self.etiqueta_info.config(text="¡Puzzle resuelto!")
                self.movimientos_solucion = []
            else:
                restantes = len(self.movimientos_solucion) - self.indice_mov
                self.etiqueta_info.config(
                    text=f"Paso {self.indice_mov}/{len(self.movimientos_solucion)}: {mov}. {restantes} pasos restantes."
                )
# ========== FUNCIÓN PRINCIPAL ==========
def principal():
    ventana = tk.Tk()
    app = InterfazPuzzle8(ventana)
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ventana.winfo_width()) // 2
    y = (ventana.winfo_screenheight() - ventana.winfo_height()) // 2
    ventana.geometry(f"+{x}+{y}")
    ventana.mainloop()
# ========== PUNTO DE ENTRADA ==========
if __name__ == "__main__":
    principal()