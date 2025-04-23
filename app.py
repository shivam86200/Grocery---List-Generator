from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

food_descriptions = {
    # Desserts
    "rasgulla": "A popular Bengali sweet made from cottage cheese (chena) balls cooked in light sugar syrup. Soft, spongy, and melt-in-your-mouth delicious. Famous in West Bengal and Odisha.",
    "gulab jamun": "Deep-fried milk solid balls soaked in rose-flavored sugar syrup. Rich, sweet, and a classic Indian dessert. Popular across India, especially in North India.",
    "kaju katli": "Diamond-shaped cashew fudge with a silvery coating. Made from ground cashews and sugar, it's smooth and creamy. A premium sweet from North India.",
    "jalebi": "Crispy, pretzel-shaped sweet made from fermented batter, deep-fried and soaked in saffron sugar syrup. Known for its bright orange color.",
    "rasmalai": "Flattened cottage cheese balls in creamy, cardamom-flavored milk. Garnished with pistachios and saffron.",
    "chamcham": "Oval-shaped Bengali sweet made from cottage cheese, soaked in cream and sugar syrup. Often decorated with coconut flakes.",
    "pantua": "Similar to gulab jamun but with a different texture, made with khoya and flour, deep-fried and soaked in sugar syrup.",
    "mishti doi": "Sweet Bengali-style yogurt, fermented and caramelized. Has a rich, creamy texture and caramel flavor.",
    "sondesh": "Traditional Bengali sweet made from cottage cheese and sugar, can be flavored with cardamom, saffron, or pistachios.",
    
    # Main Course
    "dal makhani": "A rich, creamy black lentil dish cooked with butter and cream. Originated in Punjab and now famous worldwide as a staple of North Indian cuisine. Takes 24-48 hours to prepare traditionally.",
    "butter chicken": "Creamy, mild curry made with tandoori chicken in a rich tomato-based sauce with butter and cream. Created in Delhi's Moti Mahal restaurant and now world-famous.",
    "roti": "Unleavened flatbread made from whole wheat flour, cooked on a tawa. A staple bread in North Indian cuisine, eaten with curries and dals.",
    "naan": "Leavened flatbread made from refined flour, traditionally cooked in a tandoor. Popular in North Indian restaurants and worldwide.",
    "palak paneer": "Cottage cheese cubes in a creamy spinach gravy. A vegetarian North Indian dish rich in iron and protein.",
    "biryani": "Fragrant rice dish layered with spices, meat or vegetables. Has many regional variations - Hyderabadi, Lucknowi, Kolkata styles are most famous.",
    "dosa": "Crispy fermented rice and lentil crepe. A South Indian breakfast staple, famous in Tamil Nadu and Karnataka.",
    "idli": "Steamed rice and lentil cakes. A healthy South Indian breakfast dish, very popular in Tamil Nadu.",
    "sambar": "Lentil-based vegetable stew with tamarind. Essential part of South Indian cuisine, especially in Tamil Nadu.",
    
    # Vegetables (Sabji)
    "aloo gobi": "Potato and cauliflower curry. A simple North Indian dry curry, popular home-cooked dish.",
    "bhindi masala": "Spiced okra/ladyfinger curry. Popular across India, especially in Punjab and Gujarat.",
    "baingan bharta": "Smoky mashed eggplant curry. A Punjab specialty made by roasting eggplant over fire.",
    "malai kofta": "Vegetable and paneer dumplings in creamy gravy. A rich North Indian vegetarian alternative to meatballs.",
    
    # Non-Vegetarian
    "chicken tikka masala": "Grilled chicken pieces in spiced tomato-cream sauce. Britain's national dish, adapted from Indian cuisine.",
    "fish curry": "Fresh fish cooked in a spicy, tangy curry sauce. Each coastal region has its version - Bengali, Goan, Kerala styles are famous.",
    "mutton rogan josh": "Kashmiri-style lamb curry with distinctive red color. A signature dish from Kashmir valley.",
    "tandoori chicken": "Yogurt and spice marinated chicken cooked in tandoor. Invented in Peshawar, popularized in Punjab.",
    
    # Breads
    "paratha": "Flaky, layered flatbread. Popular breakfast in North India, often stuffed with potatoes, cauliflower, or paneer.",
    "puri": "Deep-fried puffy bread. Popular across India, traditionally served for breakfast or with special meals.",
    "kulcha": "Leavened bread with or without stuffing. A specialty of Amritsar, Punjab.",
    
    # Rice Dishes
    "pulao": "Mildly spiced rice with vegetables or meat. A lighter alternative to biryani, popular across India.",
    "jeera rice": "Cumin-flavored rice. Simple but aromatic, commonly served in North Indian restaurants.",
    "lemon rice": "Tangy rice with lemon and peanuts. A South Indian specialty, popular in Tamil Nadu and Karnataka.",
    
    # Street Food
    "pani puri": "Hollow crispy balls filled with spicy water. Famous street food, known as golgappa in North India and puchka in Bengal.",
    "vada pav": "Spiced potato patty in bread roll. Mumbai's iconic street food.",
    "samosa": "Fried pastry with spiced potato filling. Popular snack across India, best known in North Indian style.",
    
    # Breakfast Items
    "poha": "Flattened rice with spices and peanuts. Popular breakfast in Maharashtra and Madhya Pradesh.",
    "upma": "Semolina porridge with vegetables. Common South Indian breakfast.",
    "pav bhaji": "Spiced mixed vegetable mash with bread rolls. Mumbai's famous street food-turned-mainstream dish.",
    
    # Vegetables
    "spinach": "Nutrient-rich leafy green vegetable, excellent source of iron and vitamins. Great for salads and cooking.",
    "broccoli": "Green vegetable with dense, tree-like florets. High in fiber and vitamins, great steamed or stir-fried.",
    "carrots": "Sweet, crunchy root vegetable rich in beta-carotene. Can be eaten raw or cooked.",
    "tomatoes": "Versatile fruit used as a vegetable, rich in lycopene. Essential in many dishes and salads.",
    
    # Non-veg
    "chicken curry": "Flavorful dish made with tender chicken pieces cooked in aromatic Indian spices and rich gravy.",
    "fish curry": "Fresh fish cooked in a spicy, tangy curry sauce. Often made with mustard oil in Bengali cuisine.",
    "mutton curry": "Slow-cooked goat meat in a rich, spicy gravy. A hearty and flavorful dish.",
    "butter chicken": "Creamy, mild curry made with tandoori chicken in a rich tomato-based sauce with butter and cream.",
    "chicken biryani": "Fragrant rice dish cooked with marinated chicken, aromatic spices, and caramelized onions.",
    "fish fry": "Crispy fried fish marinated in spices, perfect as an appetizer or side dish.",
    
    # Sugar Options
    "white sugar": "Regular refined sugar, most common sweetener used in cooking and baking.",
    "brown sugar": "Sugar with molasses content, giving a rich flavor perfect for baking.",
    "honey": "Natural sweetener made by bees, rich in antioxidants and has antimicrobial properties.",
    "jaggery": "Traditional unrefined sugar made from sugarcane, rich in minerals.",
    
    # Sugarless Options
    "stevia": "Natural zero-calorie sweetener derived from the stevia plant leaves.",
    "monk fruit sweetener": "Zero-calorie natural sweetener that's 150-200 times sweeter than sugar.",
    "erythritol": "Sugar alcohol that has almost zero calories and doesn't affect blood sugar.",
    "xylitol": "Natural sugar substitute that looks and tastes like sugar but has fewer calories.",
    
    # More Desserts
    "kheer": "Rich Indian rice pudding made with milk, rice, and cardamom, garnished with nuts.",
    "barfi": "Dense milk-based sweet fudge that can be flavored with various ingredients.",
    "ladoo": "Ball-shaped sweets made from flour, sugar, and ghee, popular during festivals.",
    "kulfi": "Traditional Indian ice cream made with thickened milk and flavored with cardamom and nuts.",
    "halwa": "Sweet confection made from various ingredients like carrots, semolina, or beetroot.",
    "payasam": "South Indian sweet pudding made with milk, rice/vermicelli, and dry fruits."
}

grocery_categories = {
    "veg": [
        # Fresh Vegetables
        "carrots", "tomatoes", "onions", "potatoes", "lettuce", "spinach", "broccoli", "cauliflower", "peas", "mushrooms",
        "bell peppers", "cucumber", "zucchini", "eggplant", "okra", "bitter gourd", "bottle gourd", "ridge gourd", "green beans", "corn",
        # Indian Vegetables
        "bhindi", "lauki", "karela", "tinda", "arbi", "methi leaves", "palak", "bathua", "sarson ka saag", "lotus root"
    ],
    "non-veg": [
        # Chicken Dishes
        "chicken curry", "butter chicken", "tandoori chicken", "chicken biryani",
        "chicken tikka masala", "chicken kebab", "chicken 65", "chicken korma",
        # Fish and Seafood
        "fish curry", "fish fry", "prawn curry", "fish tikka",
        "grilled fish", "fish biryani", "seafood platter",
        # Mutton Dishes
        "mutton curry", "mutton biryani", "keema matar", "mutton korma",
        "mutton rogan josh", "mutton seekh kebab",
        "mutton chops", "mutton keema", "mutton liver",
        "mutton ribs", "mutton leg", "mutton brain", "mutton bones", "mutton paya",
        # Fish & Seafood
        "pomfret fish", "rohu fish", "surmai fish", "bangda fish", "prawns",
        "fish fillet", "fish curry cut", "crab", "squid", "mussels",
        # Eggs & Others
        "egg tray", "quail eggs", "duck meat", "turkey meat", "rabbit meat"
    ],
    "vegan": [
        # Protein Sources
        "tofu", "tempeh", "seitan", "textured vegetable protein", "jackfruit meat",
        "soy chunks", "mushroom meat", "pea protein", "beyond meat burger", "impossible meat",
        # Dairy Alternatives
        "almond milk", "soy milk", "oat milk", "coconut milk", "cashew milk",
        "vegan cheese", "vegan butter", "vegan yogurt", "vegan cream", "vegan ice cream",
        # Other Vegan Items
        "nutritional yeast", "aquafaba", "chia seeds", "flax seeds", "hemp seeds"
    ],
    "breakfast": [
        # Hot Items
        "oatmeal", "poha", "upma", "idli", "dosa batter",
        "paratha", "bread", "pancake mix", "waffles", "french toast mix",
        # Cold Items
        "cereal", "muesli", "granola", "cornflakes", "fruit loops",
        # Beverages
        "coffee", "tea", "green tea", "milk", "juice",
        # Spreads
        "butter", "jam", "peanut butter", "honey", "nutella"
    ],
    "lunch": [
        # Main Course
        "rice", "dal", "roti", "naan", "biryani",
        "rajma", "chole", "sambar", "rasam", "curry",
        # Side Dishes
        "pickle", "papad", "chutney", "raita", "salad",
        # Quick Meals
        "sandwiches", "wraps", "pasta", "noodles", "pizza"
    ],
    "dinner": [
        # Indian Main Course
        "dal makhani", "paneer butter masala", "chicken curry", "fish curry", "mutton curry",
        "biryani", "pulao", "jeera rice", "naan", "roti",
        # International
        "pasta", "pizza", "burger", "steak", "grilled chicken",
        # Sides
        "soup", "salad", "garlic bread", "mashed potatoes", "grilled vegetables"
    ],
    "dessert": [
        # Bengali Sweets
        "rasgulla", "chamcham", "pantua", "mishti doi", "sondesh",
        # North Indian Sweets
        "gulab jamun", "jalebi", "rasmalai", "kaju katli",
        "barfi", "ladoo", "halwa", "kheer", "kulfi",
        # South Indian Sweets
        "payasam", "mysore pak", "double ka meetha",
        # Other Desserts
        "ice cream", "cake", "pastry", "cookies", "muffins"
    ],
    "sugar": [
        # Regular Sugars
        "white sugar", "brown sugar", "powdered sugar", "caster sugar",
        # Natural Sweeteners
        "honey", "jaggery", "maple syrup", "date syrup",
        "coconut sugar", "palm sugar", "molasses"
    ],
    "sugarless": [
        # Natural Zero-Calorie Sweeteners
        "stevia", "monk fruit sweetener", 
        # Sugar Alcohols
        "erythritol", "xylitol", "sorbitol",
        # Artificial Sweeteners
        "splenda", "equal", "sweet'n low", "aspartame"
    ]
}

def is_food_related(text):
    # Check if the input is directly in our food descriptions
    if text.lower() in food_descriptions:
        return True
        
    # Check common food-related words
    food_related_words = [
        'food', 'meal', 'dish', 'cuisine', 'recipe', 'cook', 'eat', 'breakfast', 'lunch', 'dinner',
        'snack', 'dessert', 'sweet', 'spicy', 'curry', 'bread', 'rice', 'roti', 'sabji', 'vegetable',
        'meat', 'chicken', 'fish', 'mutton', 'veg', 'non-veg', 'vegan', 'restaurant', 'kitchen',
        'healthy', 'tasty', 'delicious', 'traditional', 'street food', 'homemade', 'gravy', 'masala',
        'fry', 'roast', 'bake', 'grill', 'steam', 'boil', 'appetizer', 'starter', 'main course',
        'side dish', 'beverage', 'drink', 'juice', 'milk', 'tea', 'coffee'
    ]
    
    text_lower = text.lower()
    
    # Check if any food-related word is in the input
    for word in food_related_words:
        if word in text_lower:
            return True
            
    # Check if the input matches any item in our grocery categories
    for category in grocery_categories.values():
        for item in category:
            if item.lower() in text_lower:
                return True
                
    return False

def generate_grocery_list(user_input):
    user_input = user_input.lower()
    
    # First check if the input matches any food item in our descriptions
    if user_input in food_descriptions:
        return {
            "success": True,
            "message": f"Here's what I found about '{user_input}':",
            "sections": [
                {
                    "title": "Food Description",
                    "items": [food_descriptions[user_input]],
                    "type": "description"
                }
            ]
        }
    
    # Check for partial matches in food descriptions
    matching_foods = []
    for food, desc in food_descriptions.items():
        if user_input in food or food in user_input:
            matching_foods.append({"name": food, "description": desc})
    
    if matching_foods:
        return {
            "success": True,
            "message": f"Here are some related food items:",
            "sections": [
                {
                    "title": "Food Descriptions",
                    "items": [f"{food['name']}: {food['description']}" for food in matching_foods],
                    "type": "description"
                }
            ]
        }

    # Map common variations to category names
    category_mapping = {
        "vegetarian": "veg",
        "vegetables": "veg",
        "veggies": "veg",
        "healthy": "veg",  # Added mapping for 'healthy'
        "non vegetarian": "non-veg",
        "meat": "non-veg",
        "nonveg": "non-veg",
        "non veg": "non-veg",
        "plant based": "vegan",
        "sweet": "dessert",
        "sweets": "dessert",
        "morning": "breakfast",
        "evening": "dinner",
        "afternoon": "lunch",
        "sugary": "sugar",
        "sugar free": "sugarless",
        "no sugar": "sugarless",
        "diabetic": "sugarless"
    }
    
    # Find matching category
    matched_categories = []
    user_input = ' ' + user_input + ' '  # Add spaces to help with whole word matching
    
    # Direct category matches
    for category in grocery_categories.keys():
        if f" {category} " in user_input:
            matched_categories.append(category)
    
    # Check for variations
    for variation, category in category_mapping.items():
        if f" {variation} " in user_input:
            matched_categories.append(category)
            
    # Special case for single-word exact matches
    user_words = user_input.strip().split()
    if len(user_words) == 1:
        word = user_words[0]
        if word in grocery_categories:
            matched_categories.append(word)
        for variation, category in category_mapping.items():
            if word == variation:
                matched_categories.append(category)
    
    # Remove duplicates
    matched_categories = list(set(matched_categories))
    
    # If categories found, return items from all matched categories
    if matched_categories:
        sections = []
        for category in matched_categories:
            title = category.replace("-", " ").title()
            items = grocery_categories[category]
            
            # If query contains 'healthy', prioritize healthy items
            if 'healthy' in user_input:
                if category == 'veg':
                    healthy_items = [
                        "spinach", "broccoli", "kale", "carrots", "sweet potatoes",
                        "bell peppers", "tomatoes", "cucumber", "lettuce", "peas",
                        "green beans", "asparagus", "brussels sprouts", "cauliflower", "quinoa"
                    ]
                    items = healthy_items
                elif category == 'non-veg':
                    healthy_items = [
                        "chicken breast", "salmon", "tuna", "turkey breast", "egg whites",
                        "lean beef", "cod fish", "sardines", "tilapia", "shrimp"
                    ]
                    items = healthy_items
            
            sections.append({
                "title": f"{title} Items",
                "items": items,
                "type": category
            })
            
            # If category is non-veg, add complementary vegetables
            if category == 'non-veg':
                complementary_veggies = [
                    "onions", "tomatoes", "potatoes", "garlic", "ginger",
                    "green chilies", "coriander leaves", "mint leaves", "curry leaves",
                    "bell peppers", "carrots", "lemon"
                ]
                sections.append({
                    "title": "Recommended Vegetables",
                    "items": complementary_veggies,
                    "type": "veg"
                })
        return {
            "success": True,
            "message": f"Here's your grocery list:",
            "sections": sections
        }
    
    # If no category matched but the input is 'healthy', return a healthy food list
    if 'healthy' in user_input:
        return {
            "success": True,
            "message": "Here's a list of healthy food items:",
            "sections": [
                {
                    "title": "Healthy Vegetables",
                    "items": [
                        "spinach", "broccoli", "kale", "carrots", "sweet potatoes",
                        "bell peppers", "tomatoes", "cucumber", "lettuce", "peas"
                    ],
                    "type": "veg"
                },
                {
                    "title": "Healthy Proteins",
                    "items": [
                        "chicken breast", "salmon", "tuna", "turkey breast", "egg whites",
                        "lean beef", "cod fish", "sardines", "tilapia", "shrimp"
                    ],
                    "type": "non-veg"
                },
                {
                    "title": "Healthy Grains & Seeds",
                    "items": [
                        "quinoa", "brown rice", "oats", "chia seeds", "flax seeds",
                        "whole grain bread", "buckwheat", "millet", "amaranth", "wild rice"
                    ],
                    "type": "vegan"
                }
            ]
        }
    
    # If no category matched, try to get recommendations from Spoonacular API
    api_results = get_spoonacular_recommendations(user_input)
    if api_results:
        return {
            "success": True,
            "message": f"Here are some suggested ingredients for '{user_input}':",
            "sections": [
                {
                    "title": "API Recommendations",
                    "items": api_results,
                    "type": "api"
                }
            ]
        }
    
    return {
        "success": False,
        "error": "Please ask about food-related items or use categories like: \n" +
                 "- 'veg' or 'vegetarian'\n" +
                 "- 'non-veg' or 'meat'\n" +
                 "- 'vegan' or 'plant based'\n" +
                 "- 'breakfast', 'lunch', or 'dinner'\n" +
                 "- 'dessert' or 'sweets'\n" +
                 "- 'sugar' or 'sugarless'"
    }

def get_spoonacular_recommendations(query):
    try:
        api_key = os.getenv('SPOONACULAR_API_KEY')
        if not api_key:
            print("Warning: SPOONACULAR_API_KEY not found in environment variables")
            return ['Please set up your SPOONACULAR_API_KEY in the .env file']

        url = f"https://api.spoonacular.com/food/ingredients/autocomplete"
        params = {
            'apiKey': api_key,
            'query': query,
            'number': 10
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json()
            
            if not results:
                return None
                
            return [item['name'] for item in results]
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {str(e)}")
            return None
                
    except requests.RequestException as e:
        print(f"Error calling Spoonacular API: {str(e)}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_list', methods=['POST'])
def get_grocery_list():
    try:
        # Get the raw data from the request
        data = request.get_data()
        if not data:
            return jsonify({
                "success": False, 
                "error": "Please enter your food-related query."
            }), 400

        # Try to parse as JSON
        try:
            json_data = request.get_json()
        except Exception:
            return jsonify({
                "success": False, 
                "error": "Invalid request format. Please try again."
            }), 400

        # Validate the message field
        if not json_data or 'message' not in json_data:
            return jsonify({
                "success": False, 
                "error": "Please type your food-related query and try again."
            }), 400

        user_input = json_data['message'].strip()
        if not user_input:
            return jsonify({
                "success": False, 
                "error": "Please enter what kind of groceries you need."
            }), 400

        if not isinstance(user_input, str):
            return jsonify({
                "success": False, 
                "error": "Please enter text only."
            }), 400

        # Check if input is food-related
        if not is_food_related(user_input):
            return jsonify({
                "success": False,
                "error": "Please ask about food-related items. Try these categories:\n" +
                        "🥗 Vegetables (veg, vegetarian)\n" +
                        "🍖 Meat (non-veg)\n" +
                        "🌱 Plant-based (vegan)\n" +
                        "🍳 Meals (breakfast, lunch, dinner)\n" +
                        "🍰 Sweets (dessert)\n" +
                        "🍯 Sugar options (sugar, sugarless)"
            }), 400

        # Generate the grocery list
        result = generate_grocery_list(user_input)
        
        # If the result indicates an error, return it with 400 status
        if not result.get("success", True):
            return jsonify(result), 400
            
        return jsonify(result)

    except Exception as e:
        print(f"Error in get_grocery_list: {str(e)}")
        return jsonify({
            "success": False, 
            "error": "An unexpected error occurred. Please try again with a different query."
        }), 500

@app.route('/get_food_details/<food_name>', methods=['GET'])
def get_food_details(food_name):
    food_name = food_name.lower()
    if food_name in food_descriptions:
        return jsonify({
            "success": True,
            "name": food_name,
            "description": food_descriptions[food_name]
        })
    return jsonify({
        "success": False,
        "error": "Food item not found"
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
