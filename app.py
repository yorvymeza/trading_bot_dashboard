from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta # Importamos timedelta
from trading_logic import TradingBot # ⬅️ IMPORTAR LA CLASE DESDE EL NUEVO ARCHIVO

app = Flask(__name__)

# ===============================================
# 🤖 INICIALIZACIÓN DEL BOT
# ===============================================

# Inicializar el bot
bot = TradingBot()


# ===============================================
# ⚙️ CONTEXT PROCESSOR (SOLUCIÓN AL ERROR)
# ===============================================

@app.context_processor
def inject_global_variables():
    """
    Inyecta el objeto 'bot' en el contexto de TODAS las plantillas.
    Esto soluciona el error 'jinja2.exceptions.UndefinedError: 'bot' is undefined'.
    """
    return dict(
        bot=bot,
        now=datetime.now()
    )


# ===============================================
# 📊 FUNCIONES DE UTILIDAD (Fuera de la clase)
# ===============================================

def get_history_stats(history_list):
    """Calcula las estadísticas para una lista de operaciones (ej. Hoy, Semana, Todo)."""
    total_ops = len(history_list)
    total_wins = sum(1 for op in history_list if op['result'] == 'WIN')
    total_losses = total_ops - total_wins
    net_profit = sum(op['profit'] for op in history_list)
    
    return {
        'total_operations': total_ops,
        'total_wins': total_wins,
        'total_losses': total_losses,
        'net_profit': f'{"+" if net_profit >= 0 else ""}{round(net_profit, 2)}'
    }

def get_filtered_history(period='all'):
    """Filtra el historial del bot por periodo."""
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    week_ago = (now - timedelta(days=7)).strftime('%Y-%m-%d')
    month_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    
    if period == 'dia':
        filtered = [op for op in bot.history if op['date'] == today_str]
    elif period == 'semana':
        filtered = [op for op in bot.history if op['date'] >= week_ago]
    elif period == 'mes':
        filtered = [op for op in bot.history if op['date'] >= month_ago]
    else: # 'todo'
        filtered = bot.history
        
    stats = get_history_stats(filtered)
    stats['operations'] = filtered
    
    return stats


# ===============================================
# 🌐 VISTAS DE FLASK PARA LA INTERFAZ WEB
# ===============================================

@app.route('/')
def dashboard():
    # Obtener datos de HOY para el Dashboard
    today_history = get_filtered_history(period='dia')
    
    # Simular datos para el dashboard
    dashboard_data = {
        'total_balance': f'${round(bot.balance, 2)}',
        'bot_active': bot.is_active,
        'balance_change': '+12.5%', 
        'operations_today': today_history['total_operations'],
        'wins_today': today_history['total_wins'],
        'losses_today': today_history['total_losses'],
        'success_rate': round(today_history['total_wins'] / today_history['total_operations'] * 100) if today_history['total_operations'] > 0 else 0,
        'next_operation_time': '2m 15s',
        'next_operation_pair': 'EUR/USD',
        'next_operation_type': 'CALL',
        'bot_status': 'Actualmente ejecutando operaciones' if bot.is_active else 'Inactivo, esperando comando.',
        'operation_amount': f'${bot.default_amount}',
        'time_between_operations': '5 minutos',
        'current_asset': 'EUR/USD',
        'last_operations': today_history['operations'][:4] 
    }
    
    # Ya no necesitamos pasar 'bot=bot' aquí gracias al context processor
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/toggle', methods=['POST'])
def toggle():
    """Ruta para activar/desactivar el bot desde la web."""
    bot.toggle_bot()
    return redirect(url_for('dashboard'))

@app.route('/execute_manual_entry', methods=['POST'])
def execute_manual_entry():
    """Ruta para ejecutar una entrada manual."""
    pair = request.form.get('pair')
    entry_type = request.form.get('entry_type')
    amount = float(request.form.get('amount'))
    duration = request.form.get('duration')
    
    # El bot se encarga de la ejecución y el registro
    bot.execute_entry(pair, entry_type, amount, duration)
    return redirect(url_for('dashboard'))


# Rutas del Historial
@app.route('/history')
def history_dia():
    data = get_filtered_history(period='dia')
    return render_template('history.html', data=data, active_period='Hoy')

@app.route('/history/semana')
def history_semana():
    data = get_filtered_history(period='semana')
    return render_template('history.html', data=data, active_period='Esta Semana')

@app.route('/history/mes')
def history_mes():
    data = get_filtered_history(period='mes')
    return render_template('history.html', data=data, active_period='Este Mes')

@app.route('/history/todo')
def history_todo():
    data = get_filtered_history(period='todo')
    return render_template('history.html', data=data, active_period='Todo')


@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/cuenta')
def cuenta():
    # Simular datos de la cuenta
    cuenta_data = {
        'current_balance': f'${round(bot.balance, 2)}',
        'account_type': 'Real',
        'broker_status': 'Conectado',
        'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render_template('cuenta.html', data=cuenta_data)


if __name__ == '__main__':
    app.run(debug=True)