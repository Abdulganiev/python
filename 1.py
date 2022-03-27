total_web = 10
total_speakers = 7539

chinese_speakers = 1107 
chinese_web_part = 0.017
english_speakers = 1121
english_web_part = 0.539
russian_speakers = 264.3
russian_web_part = 0.061
print('--- Китайский язык ---')
print('Доля говорящих на языке: ',chinese_speakers*100/total_speakers,'%')
print('Доля сайтов с языком: ',chinese_web_part*100/total_web,'%')
print('Индекс проникновения в интернет: ',chinese_web_part/chinese_speakers)

print('--- Английский язык ---')
print('Доля говорящих на языке: ',english_speakers*100/total_speakers,'%')
print('Доля сайтов с языком: ',english_web_part*100/total_web,'%')
print('Индекс проникновения в интернет: ',english_web_part/english_speakers)

print('--- Русский язык ---')
print('Доля говорящих на языке: ',russian_speakers*100/total_speakers,'%')
print('Доля сайтов с языком: ',russian_web_part*100/total_web,'%')
print('Индекс проникновения в интернет: ',english_web_part/russian_web_part)
