import os
import csv
from django.utils import timezone
from datetime import timedelta
from users.models import Profile
from decks.models import Deck, FlashCard  # مطمئن شوید نام اپلیکیشن صحیح است
import django

# تنظیم محیط Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YourProjectName.settings')  # نام پروژه خود را وارد کنید
django.setup()

def import_flashcards(csv_file_path):
    try:
        # باز کردن فایل CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # خواندن داده‌ها به عنوان دیکشنری
            
            # بررسی وجود ستون‌های ضروری
            required_fields = {'Word', 'Translation', 'Example', 'Example Translation'}
            if not required_fields.issubset(reader.fieldnames):
                raise ValueError(f"CSV file is missing required columns: {required_fields - set(reader.fieldnames)}")

            # ایجاد Deck و FlashCard برای هر کاربر
            for profile in Profile.objects.all():
                # ایجاد یک Deck جدید برای کاربر
                deck = Deck.objects.create(
                    owner=profile,
                    name="New Deck",
                    description="Imported Flashcards",
                    language="english",
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                )

                print(f"Created Deck for {profile.user.username}")

                # بازخوانی فایل CSV برای هر کاربر
                file.seek(0)  # بازنشانی موقعیت فایل
                next(reader)  # رد کردن هدر CSV

                # ایجاد فلش‌کارت‌ها
                for row in reader:
                    try:
                        FlashCard.objects.create(
                            deck=deck,
                            front=f"<h2>{row['Word']}</h2><p>{row['Example']}</p>",
                            back=f"<h2>{row['Translation']}</h2><p>{row['Example Translation']}</p>",
                            next_review=timezone.now(),
                            interval_day=1,
                            difficulty=2.5
                        )
                    except Exception as e:
                        print(f"Error creating FlashCard for word '{row['Word']}': {e}")
                        continue

                print(f"FlashCards added to Deck for {profile.user.username}")

        print("Import process completed successfully!")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# اجرای اسکریپت
import_flashcards('data/english_flashcards.csv')  # مسیر فایل CSV را وارد کنید
