"""
Script para gestionar la base de datos y migraciones.
Proporciona comandos para crear, migrar y gestionar la base de datos.
"""
import argparse
import os
import sys
import subprocess

def run_command(command):
    """Ejecutar un comando y mostrar su salida."""
    print(f"Ejecutando: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    
    return process.returncode

def create_migration(message):
    """Crear una nueva migración con Alembic."""
    return run_command(f"python -m alembic revision --autogenerate -m \"{message}\"")

def apply_migrations():
    """Aplicar todas las migraciones pendientes."""
    return run_command("python -m alembic upgrade head")

def rollback_migration(steps=1):
    """Revertir una o más migraciones."""
    if steps == 0:
        print("El número de pasos debe ser mayor que 0.")
        return 1
    
    if steps > 0:
        return run_command(f"python -m alembic downgrade -{steps}")
    else:
        # Si steps es negativo, lo tratamos como "revertir todo"
        return run_command("python -m alembic downgrade base")

def show_history():
    """Mostrar el historial de migraciones."""
    return run_command("python -m alembic history")

def show_current():
    """Mostrar la revisión actual de la base de datos."""
    return run_command("python -m alembic current")

def create_tables_direct():
    """Crear tablas directamente con SQL (usando script create_tables_direct.py)."""
    return run_command("python create_tables_direct.py")

def main():
    """Función principal que procesa los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Gestionar la base de datos y migraciones.")
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando para crear una nueva migración
    create_parser = subparsers.add_parser("create", help="Crear una nueva migración")
    create_parser.add_argument("message", help="Mensaje descriptivo para la migración")
    
    # Comando para aplicar migraciones
    subparsers.add_parser("migrate", help="Aplicar todas las migraciones pendientes")
    
    # Comando para revertir migraciones
    rollback_parser = subparsers.add_parser("rollback", help="Revertir migraciones")
    rollback_parser.add_argument("--steps", type=int, default=1, help="Número de migraciones a revertir")
    
    # Comando para mostrar el historial de migraciones
    subparsers.add_parser("history", help="Mostrar el historial de migraciones")
    
    # Comando para mostrar la revisión actual
    subparsers.add_parser("current", help="Mostrar la revisión actual de la base de datos")
    
    # Comando para crear tablas directamente con SQL
    subparsers.add_parser("create-tables", help="Crear tablas directamente con SQL")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return create_migration(args.message)
    elif args.command == "migrate":
        return apply_migrations()
    elif args.command == "rollback":
        return rollback_migration(args.steps)
    elif args.command == "history":
        return show_history()
    elif args.command == "current":
        return show_current()
    elif args.command == "create-tables":
        return create_tables_direct()
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
