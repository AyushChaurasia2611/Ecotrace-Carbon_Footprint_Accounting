import os
from app import app, db, User, CommuteLog, TreePlantation, Event, EventParticipant, Notification, Achievement, UserAchievement, Challenge, ChallengeParticipant

def migrate():
    output_lines = []
    tables = ['user', 'commute_log', 'tree_plantation', 'notification', 'challenge', 'achievement', 'user_achievement', 'event', 'event_participant', 'activity_log']
    sqlite_path = 'instance/ecotrace.db'
    
    if not os.path.exists(sqlite_path):
        output_lines.append(f"❌ SQLite file not found at {sqlite_path}")
        return

    output_lines.append("--- Reading data from local ecotrace.db (SQLite) with sqlite3 ---")
    import sqlite3
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {}
    for t in tables:
        try:
             cursor.execute(f"SELECT * FROM {t}")
             data[t] = [dict(row) for row in cursor.fetchall()]
             output_lines.append(f"-> Found {len(data[t])} rows in {t}")
        except Exception as e:
             output_lines.append(f"Skipping table {t} reading: {e}")
             data[t] = []
    conn.close()

    # Point to Supabase/Postgres loaded from .env
    with app.app_context():
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            output_lines.append("❌ Error: DATABASE_URL not found in environment")
            return
            
        if db_url.startswith("postgres://"):
             db_url = db_url.replace("postgres://", "postgresql://", 1)
             
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        output_lines.append("\n--- Connecting to Supabase and Migrating ---")
        
        # ✅ Ensure tables exist on Supabase
        db.create_all()
        output_lines.append("✅ Database tables created/verified on Supabase")
        
        from sqlalchemy.exc import IntegrityError

        def migrate_table(name, model_cls):
            count = 0
            table_name = model_cls.__tablename__
            rows = data.get(table_name, [])
            
            for row in rows:
                try:
                    # ✅ Safe mapping uses constructors with defaults
                    if name == "User":
                         item = User(username=row.get('username', ''), password_hash=row.get('password_hash', ''))
                    else:
                         try:
                              item = model_cls()
                         except TypeError as e:
                              if "missing" in str(e) and ("argument" in str(e) or "positional" in str(e)):
                                   import inspect
                                   spec = inspect.getfullargspec(model_cls.__init__)
                                   args = spec.args[1:] if spec.args else []
                                   required_count = len(args) - len(spec.defaults) if spec.defaults else len(args)
                                   kwargs = {a: None for a in args[:required_count]}
                                   item = model_cls(**kwargs)
                              else:
                                   raise e
                         
                    for key, value in row.items():
                         setattr(item, key, value)
                         
                    db.session.add(item)
                    db.session.commit()  # Individual commit to skip duplicates
                    count += 1
                except IntegrityError as e:
                    db.session.rollback()  # Skip already seeded/duplicate items
                    output_lines.append(f"⚠️ Skipping a {name} due to IntegrityError: {e}")
                except Exception as e:
                    db.session.rollback()
                    output_lines.append(f"❌ Skipping a {name} due to unexpected error: {e}")
            output_lines.append(f"✅ Migrated {count}/{len(rows)} {name}s")

        migrate_table("User", User)
        migrate_table("CommuteLog", CommuteLog)
        migrate_table("TreePlantation", TreePlantation)
        migrate_table("Event", Event)
        migrate_table("EventParticipant", EventParticipant)
        migrate_table("Notification", Notification)
        migrate_table("Achievement", Achievement)
        migrate_table("UserAchievement", UserAchievement)
        migrate_table("Challenge", Challenge)
        migrate_table("ChallengeParticipant", ChallengeParticipant)
        from app import ActivityLog
        migrate_table("ActivityLog", ActivityLog)

        output_lines.append("\n✅ Migration complete! Multiples might have skipped if already seeded.")
        
        # Write report to file
        with open('migrate_output.txt', 'w', encoding='utf-8') as f:
             f.write("\n".join(output_lines))
             
        return

if __name__ == '__main__':
    migrate()
