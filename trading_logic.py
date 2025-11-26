from datetime import datetime
import random
import time

class TradingBot:
    """Clase principal para la lógica de trading y manejo de operaciones."""
    
    def __init__(self, initial_balance=1000.0, default_amount=50.0):
        # Configuración básica
        self.is_active = False
        self.balance = initial_balance
        self.default_amount = default_amount
        self.operation_id_counter = 500 # Para IDs simulados
        
        # Historial de operaciones (simulado)
        self.history = self._load_initial_history()

    def _load_initial_history(self):
        """Carga datos iniciales para simular un historial completo (Todo)."""
        return [
            {'id': 'OP500', 'date': '2023-12-25', 'time': '09:10:00', 'pair': 'EUR/USD', 'type': 'CALL', 'amount': 50.00, 'duration': '5m', 'result': 'WIN', 'profit': 37.50},
            {'id': 'OP499', 'date': '2023-12-24', 'time': '16:05:00', 'pair': 'GBP/USD', 'type': 'PUT', 'amount': 50.00, 'duration': '5m', 'result': 'LOSS', 'profit': -50.00},
            {'id': 'OP498', 'date': '2023-12-23', 'time': '11:50:00', 'pair': 'USD/JPY', 'type': 'CALL', 'amount': 50.00, 'duration': '5m', 'result': 'WIN', 'profit': 38.75},
            {'id': 'OP497', 'date': '2023-12-22', 'time': '13:40:00', 'pair': 'EUR/USD', 'type': 'PUT', 'amount': 50.00, 'duration': '5m', 'result': 'WIN', 'profit': 42.00}
        ]

    def toggle_bot(self):
        """Activa o desactiva el bot."""
        self.is_active = not self.is_active
        print(f"Bot {'ACTIVADO' if self.is_active else 'DESACTIVADO'}")

    def execute_entry(self, pair, entry_type, amount, duration):
        """
        Simula la ejecución de una operación.
        Aquí es donde se integraría la librería de la plataforma.
        """
        if not self.is_active:
            print("❌ BOT DESACTIVADO. No se puede ejecutar la entrada.")
            return None

        # 1. Simular envío de la operación a la plataforma
        self.balance -= amount
        
        # 2. Simular el resultado (Para demostración: 75% WIN)
        is_win = random.random() < 0.75
        
        profit_rate = 0.75 # 75% de pago
        
        if is_win:
            profit = amount * profit_rate
            result = 'WIN'
            self.balance += (amount + profit)
        else:
            profit = -amount
            result = 'LOSS'
        
        # 3. Registrar la operación
        self.operation_id_counter += 1
        now = datetime.now()
        new_op = {
            'id': f'OP{self.operation_id_counter}',
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'pair': pair,
            'type': entry_type,
            'amount': amount,
            'duration': duration,
            'result': result,
            'profit': round(profit, 2)
        }
        
        self.history.insert(0, new_op) # Añadir al principio del historial
        print(f"✅ ENTRADA EJECUTADA: {pair} {entry_type} | Resultado: {result} | Ganancia: {round(profit, 2)}")
        return new_op