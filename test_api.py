#!/usr/bin/env python3
"""Test simple para verificar si el API funciona"""

import sys
import json
from app.models.ModeloDeClasificacionTextos import cargar_dataset, get_categories

print("🧪 Test de cargar_dataset()...")

try:
    print("  Cargando dataset...")
    dataset = cargar_dataset()
    print(f"  ✅ Dataset cargado: {len(dataset)} items")
    print(f"  Primeros 3: {dataset[:3]}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🧪 Test de get_categories()...")
try:
    cats = get_categories()
    print(f"  ✅ Categorías: {cats}")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n✅ Tests completados")
