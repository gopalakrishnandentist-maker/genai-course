# 7-day South Indian vegetarian meal plan prompt

Copy everything below into any AI chat tool. Change only the FOR block.

## FOR (edit this block only)
- Age and sex: 38, woman
- Height and weight: 158 cm, 72 kg
- Activity level: sedentary, desk job, 20 minute walk most evenings
- Allergies: none
- Dislikes: bitter gourd
- Weekday cooking time: 20 minutes for breakfast, 30 minutes for dinner
- Household: cooks for a family of four, so lunch is the family meal
- City and month: Chennai, November

## ROLE
You are a clinical nutritionist from Tamil Nadu who plans everyday home meals for South Indian families. You plan around what the family already cooks, not around diet foods.

## TASK
Write a 7-day vegetarian meal plan for the person in the FOR block, who is working towards gradual weight loss of about half a kilo a week.

## CONTEXT
- Vegetarian. Dairy is fine. No egg, meat or fish.
- Recognisably South Indian dishes cooked at home, called by their real Tamil names.
- Ingredients sold in an ordinary market in the city in the FOR block, in that month.
- Work out a daily calorie target from the FOR block for a loss of about half a kilo a week, never below 1,200 kcal. No meal except the snack under 250 kcal, no crash dieting.
- Every breakfast, lunch and dinner has a protein source: paruppu, sambar, sundal, curd, paneer, or a dal-based batter such as adai or pesarattu.
- Breakfast and dinner on Monday to Friday must fit the weekday cooking time. Slower dishes (adai, idiyappam, appam, paniyaram) go on Saturday or Sunday.
- Lunch is the family meal, so it must be a normal rice meal the whole household eats.
- No dish repeats on two days in a row.
- Leave out everything in Allergies and Dislikes, including as an ingredient inside another dish.

## FEW-SHOT (the style of row I want)
| Day | Meal | Dish | Portion |
|---|---|---|---|
| Mon | Breakfast | Idli with sambar | 3 idli, 1 katori sambar |
| Mon | Lunch | Rice, beans poriyal, keerai kootu, curd | 1 katori rice, 1 katori poriyal, 1 katori kootu, ½ katori curd |

## RESPONSE
- One markdown table with exactly these columns: Day | Meal | Dish | Portion.
- 28 rows: Monday to Sunday, each with Breakfast, Lunch, Snack, Dinner in that order.
- Portions in household measures only: idli, dosai or chapati by count, everything else in katori (one katori = 150 ml) or teaspoons.
- After the table, exactly three lines and nothing else:
  1. Daily calories: the range for this plan.
  2. Oil: total teaspoons a day.
  3. Note: this is a draft to discuss with a qualified dietitian, not medical advice.
- No introduction before the table.

## AVOID
Quinoa, avocado, kale, oats bowls, smoothies, salads as a full meal, and other imported "diet" foods. No meal replacement drinks, no skipped meals, no fasting days.
