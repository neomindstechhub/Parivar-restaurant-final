import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, ShoppingBag } from "lucide-react";
import { Link } from "@tanstack/react-router";
import logo from "@/assets/parivar-logo.png";
import { useCartStore } from "@/store/cart";
import { CartDrawer } from "./CartDrawer";
import { HalalBadge } from "./HalalBadge";

const links = [
  { label: "Home", hash: "home" },
  { label: "Today's Special", hash: "specials" },
  { label: "Menu", hash: "menu" },
  { label: "Catering", hash: "catering" },
  { label: "About", hash: "about" },
  { label: "Contact", hash: "contact" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const cartItems = useCartStore((state) => state.items);
  const cartCount = cartItems.reduce((acc, item) => acc + item.quantity, 0);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      <motion.header
        initial={{ y: -40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="fixed rounded-4xl mt-2 ml-2 mr-2 top-0 inset-x-0 z-[9999] transition-all duration-500 flex items-center px-6 md:px-10"
        style={{
          height: "90px",
          background: scrolled ? "rgba(246, 232, 215, 0.25)" : "rgba(246, 232, 215, 0.12)",
          backdropFilter: scrolled ? "blur(24px)" : "blur(16px)",
          WebkitBackdropFilter: scrolled ? "blur(24px)" : "blur(16px)",
          borderBottom: "1px solid rgba(246, 232, 215, 0.15)",
        }}
      >
        <nav className="w-full flex items-center justify-between">
          <div className="flex items-center gap-2  shrink-0">
            <Link to="/" hash="home" className="flex items-center">
              <img src={logo} alt="Parivar Restaurant — Timeless Indian Flavours" className="h-14 md:h-[4.5rem] w-auto object-contain drop-shadow-sm rounded-[50%]" />
            </Link>
            <HalalBadge className="h-20 md:h-[5.5rem]" />
          </div>

          <ul className="hidden md:flex items-center gap-10 text-[15px] font-medium tracking-wide">
            {links.map((l) => (
              <li key={l.hash}>
                <Link
                  to="/"
                  hash={l.hash}
                  className="relative block transition-all duration-300 text-[#042416] hover:text-[#D4A017] hover:-translate-y-0.5 after:content-[''] after:absolute after:-bottom-1.5 after:left-1/2 after:-translate-x-1/2 after:h-[1px] after:w-0 hover:after:w-full after:bg-[#D4A017] after:transition-all after:duration-300"
                >
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>

          <div className="flex items-center gap-4 md:gap-6">
            <Link
              to="/"
              hash="menu"
              className="hidden md:inline-flex items-center justify-center px-8 py-3 rounded-full text-sm font-semibold tracking-wider transition-all duration-300 hover:-translate-y-0.5 text-white bg-[#D4A017] hover:bg-[#E0B03D]"
            >
              ORDER NOW
            </Link>

            <button 
              onClick={() => setIsCartOpen(true)}
              className="relative p-2 text-[#042416] hover:text-[#D4A017] transition-colors flex items-center justify-center"
            >
              <ShoppingBag className="w-6 h-6" />
              {cartCount > 0 && (
                <span className="absolute top-0 right-0 translate-x-1/4 -translate-y-1/4 bg-red-600 text-white text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full shadow-sm">
                  {cartCount}
                </span>
              )}
            </button>

            <button
              aria-label="Open menu"
              onClick={() => setOpen(true)}
              className="md:hidden p-2 transition-colors hover:bg-black/5 rounded-full text-[#042416]"
            >
              <Menu className="h-7 w-7" />
            </button>
          </div>
        </nav>
      </motion.header>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[10000] flex flex-col"
            style={{
              background: "rgba(246, 232, 215, 0.95)",
              backdropFilter: "blur(20px)",
              WebkitBackdropFilter: "blur(20px)",
            }}
          >
            <div className="flex justify-between items-center p-8">
              <div className="flex items-center gap-2 md:gap-3 shrink-0">
                <img src={logo} alt="Parivar Restaurant" className="h-20 w-auto object-contain drop-shadow-sm" />
                <HalalBadge className="h-24" />
              </div>
              <button 
                onClick={() => setOpen(false)} 
                aria-label="Close menu" 
                className="p-2 rounded-full hover:bg-black/5 transition-colors text-[#042416]"
              >
                <X className="h-8 w-8" />
              </button>
            </div>
            <ul className="flex-1 flex flex-col items-center justify-center gap-10 text-3xl font-display">
              {links.map((l, i) => (
                <motion.li
                  key={l.hash}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + i * 0.07 }}
                >
                  <Link
                    to="/"
                    hash={l.hash}
                    onClick={() => setOpen(false)}
                    className="transition-colors duration-300 text-[#042416] hover:text-[#D4A017]"
                  >
                    {l.label}
                  </Link>
                </motion.li>
              ))}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Link
                  to="/"
                  hash="menu"
                  onClick={() => setOpen(false)}
                  className="mt-6 inline-block px-10 py-4 rounded-full text-base font-semibold tracking-wider text-white bg-[#D4A017]"
                >
                  ORDER NOW
                </Link>
              </motion.div>
            </ul>
          </motion.div>
        )}
      </AnimatePresence>

      <CartDrawer isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </>
  );
}
