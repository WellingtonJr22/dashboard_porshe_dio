from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
DATA_FILE = ROOT / 'data' / 'porsche_sales.json'


def clean_name(value: object) -> str:
    text = ' '.join(str(value or '').strip().split())
    return ' '.join(part[:1].upper() + part[1:].lower() for part in text.split())


def load_records(input_path: Path) -> list[dict]:
    df = pd.read_excel(input_path, sheet_name='Sanitized')
    records = []
    for _, row in df.iterrows():
        records.append({
            'id': int(row['sale_id']),
            'dateRaw': str(row['sale_date']),
            'dateSanitized': str(row['SaleDateSanitized']),
            'customer': str(row['customer_name']),
            'model': str(row['PorscheModelSanitized']),
            'year': int(row['ModelYearSanitized']),
            'price': float(row['SalesPriceSanitized']),
            'mileage': int(row['VehicleMileageSanitized']),
            'payment': str(row['PayMethodSanitized']),
            'city': str(row['CitySanitized']),
            'state': str(row['StateSanitized']).upper(),
            'seller': clean_name(row['salesperson']),
            'status': str(row['DeliveryStatusSanitized']),
        })
    return records


def update_index(records: list[dict]) -> None:
    content = INDEX.read_text(encoding='utf-8')
    replacement = 'window.PORSCHE_DATA = ' + json.dumps(records, ensure_ascii=False, separators=(',', ':')) + ';'
    pattern = r'window\.PORSCHE_DATA\s*=\s*.*?;'
    new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError('Marcador window.PORSCHE_DATA não encontrado no index.html')
    INDEX.write_text(new_content, encoding='utf-8')


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python scripts/build_dashboard.py caminho/para/base.xlsx')
    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f'Arquivo não encontrado: {input_path}')
    records = load_records(input_path)
    DATA_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    update_index(records)
    invalid = sum(r['dateSanitized'] == 'INVALID' for r in records)
    print(f'{len(records)} registros incorporados ao dashboard. Datas inválidas: {invalid}.')


if __name__ == '__main__':
    main()
