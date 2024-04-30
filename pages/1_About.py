import streamlit as st
from PIL import Image
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(page_title="Carbon Footprint",page_icon=":footprints:",layout="wide")
__login__obj = __login__(auth_token = "dk_prod_D8ZQ8GGX75M35KMST4HRTSX97QED",company_name = "Carbon Footprint Calculator",width = 200, height = 250,logout_button_name = 'Logout', hide_menu_bool = False,hide_footer_bool = False,lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

if LOGGED_IN == True:
    __login__obj.hide_menu()
    #storing images
    img_contact_form=Image.open("Images/Screenshot 2024-04-13 224751.png")

    with st.container():
        st.header("Understanding Carbon Footprint :footprints:")
        st.write("---")
    with st.container():
        text_column,image_column=st.columns((1,0.8))
        with text_column:
            st.write("Have you ever wondered about the impact of your daily actions on the environment? Imagine every time you use electricity, drive a car, or even eat food, you're leaving behind a mark on the planet. This mark is called your carbon footprint.")
            st.subheader("But what exactly is a carbon footprint?")
            st.write("Well, think of it as a measure of how much carbon dioxide and other greenhouse gases you produce as a result of your activities. These gases trap heat in the atmosphere, contributing to global warming and climate change. Your carbon footprint isn't just about the big things like driving a car or using electricity. It's also about the small everyday choices you make, like the food you eat, the products you buy, and even how you travel. For example, every time you turn on a light or watch TV, you're using electricity generated from fossil fuels like coal or natural gas. Burning these fuels releases carbon dioxide into the air, adding to your carbon footprint. Similarly, when you drive a car or take a flight, the burning of fuel releases greenhouse gases into the atmosphere, contributing to your carbon footprint. Even the food you eat has a carbon footprint, depending on how it's produced and transported.")
            st.subheader("So, why is it important to understand your carbon footprint?")
            st.write("Well, by understanding how your actions affect the environment, you can take steps to reduce your impact and live a more sustainable lifestyle. This could mean using energy more efficiently, choosing greener modes of transportation, or consuming less meat and dairy products. By reducing your carbon footprint, you're not only helping the environment but also contributing to a healthier planet for future generations. In summary, your carbon footprint is a measure of the impact your everyday actions have on the environment. By understanding and reducing your carbon footprint, you can play a part in combating climate change and creating a more sustainable world for all.")
            st.write("---")
        with image_column:
            st.image(img_contact_form)
    with st.container():
        st.header("Carbon Emissions in India")
        st.subheader("1. Air Pollution: ")
        st.write("Carbon emissions from vehicles, factories, and power plants create smog and dirty the air we breathe. This pollution can lead to health problems like asthma and lung diseases, especially in crowded cities.")
        st.subheader("2. Climate Change: ")
        st.write("When carbon dioxide and other greenhouse gases build up in the atmosphere, they trap heat and make the Earth's climate warmer. This leads to extreme weather events like floods, droughts, and heatwaves, which can harm crops, homes, and communities.")
        st.subheader("3. Health Risks: ")
        st.write("Breathing in polluted air with high levels of carbon emissions can make people sick. It can cause respiratory issues, heart problems, and even premature death, especially for vulnerable groups like children and the elderly.")
        st.subheader("4. Water Scarcity: ")
        st.write("Climate change, fueled by carbon emissions, affects rainfall patterns and leads to water shortages. This can make it harder for people to access clean water for drinking, farming, and sanitation.")
        st.subheader("5. Loss of Biodiversity: ")
        st.write("Carbon emissions contribute to habitat destruction and disrupt ecosystems, leading to loss of plant and animal species. This affects biodiversity, which is essential for a healthy environment and food security.")
        st.subheader("6. Economic Impact: ")
        st.write("The effects of carbon emissions, such as extreme weather events and health problems, can also have a big impact on the economy. It can damage infrastructure, reduce agricultural productivity, and increase healthcare costs, putting a strain on communities and businesses.")   
        st.write("---")
    with st.container():
        st.header("Reducing Your Carbon Footprint 📉")
        st.write("Following ways can be adopted to reduce your carbon footprint: ")
        st.subheader("1. Household Energy Consumption:")
        st.write("Consider using energy-efficient appliances and turning off lights when not in use to reduce electricity usage. Opt for energy-efficient cooking appliances and explore alternative cooking methods like induction cooktops to lower LPG consumption.")
        st.subheader("2. Transportation:")
        st.write("Try carpooling, using public transportation, or walking/cycling for short trips to reduce car usage. Consider consolidating trips and choosing direct flights to minimize flying emissions.")
        st.subheader("3. Food and Consumption:")
        st.write("Consume more plant-based meals, reduce food waste, and buy locally sourced produce to lower food-related emissions. Focus on reducing water consumption and using energy-efficient lighting for other utility items.")
        st.subheader("4. Travel and Lifestyle Choices:")
        st.write("Choose eco-friendly accommodations and support sustainable tour operators to minimize tourism-related emissions. Consider online courses and digital resources to reduce commuting and support educational institutions with green initiatives.")        
        st.subheader("5. Product Choices:")
        st.write("Opt for eco-friendly products with minimal packaging and consider the environmental impact of your purchasing decisions. Support companies that prioritize sustainability and choose products made from recycled materials.")
        st.subheader("6. Waste Management:")
        st.write("Reduce waste by practicing recycling, composting, and avoiding single-use items whenever possible. Support initiatives for proper waste disposal and participate in community clean-up efforts.")
        st.subheader("7. Water Conservation:")
        st.write("Conserve water by fixing leaks, using water-saving devices, and practicing water-efficient gardening techniques. Consider collecting rainwater for outdoor use and supporting water conservation programs.")
        st.subheader("8. Energy Efficiency:")
        st.write("Improve energy efficiency in your home by upgrading insulation, sealing air leaks, and installing energy-efficient windows and doors. Use programmable thermostats and smart home technology to optimize energy usage.")
        st.subheader("9. Sustainable Gardening:")
        st.write("Practice sustainable gardening techniques such as planting native species, using organic fertilizers, and minimizing pesticide use. Create habitat for wildlife and support biodiversity in your garden.")
        st.subheader("10. Community Engagement:")
        st.write("Get involved in local environmental initiatives, clean-up events, and tree planting programs to make a positive impact in your community. Advocate for sustainable practices and support policies that promote environmental conservation.")
        st.write("---")
        st.write("---")