import { useState } from "react";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import ContactModal from "@/components/ContactModal";
import Gallery from "@/components/Gallery";
import Facilities from "@/components/Facilities";
import FoodMenu from "@/components/FoodMenu";
import Rooms from "@/components/Rooms";
import Stats from "@/components/Stats";
import Feedback from "@/components/Feedback";

const Index = () => {
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <Navbar onContactClick={() => setIsContactModalOpen(true)} />
      
      <main>
        <Hero />
        <About />
        <Gallery />
        <Facilities />
        <FoodMenu />
        <Rooms />
        <Stats />
        <Feedback />
      </main>

      <ContactModal 
        isOpen={isContactModalOpen}
        onClose={() => setIsContactModalOpen(false)}
      />
      
      <footer className="bg-hostel-primary text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-xl font-bold mb-2">🏨 City Central Hostel</h3>
          <p className="text-white/80 mb-4">Your comfortable stay in the heart of the city</p>
          <p className="text-sm text-white/60">
            © 2024 City Central Hostel. All rights reserved. | Contact: +91 9876543210
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
