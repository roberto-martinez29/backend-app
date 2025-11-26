import os
from sqlalchemy import create_engine, text


try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def mask(s, prefix=12):
    if not s:
        return None
    return s[:prefix] + '...'


def main():
    # Prefer python-dotenv when available, otherwise load .env manually
    if load_dotenv:
        load_dotenv()
    else:
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k, v)

    DATABASE_URL = os.getenv('DATABASE_URL')
    print('DATABASE_URL set:', bool(DATABASE_URL))
    print('DATABASE_URL (masked):', mask(DATABASE_URL))

    if not DATABASE_URL:
        print('No DATABASE_URL found, aborting')
        return 2

    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            r = conn.execute(text('SELECT 1'))
            print('SELECT 1 ->', r.scalar())

            info = conn.execute(text("SELECT current_database(), current_user, version()"))
            print('DB info ->', info.fetchone())

            try:
                tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' LIMIT 20"))
                tbls = [t[0] for t in tables.fetchall()]
                print('Public tables (sample):', tbls)
            except Exception as e:
                print('Could not list tables:', e)

    except Exception as e:
        print('ERROR:', type(e).__name__, str(e))
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
