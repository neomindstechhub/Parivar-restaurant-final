import { resolveImageUrl } from "@/utils/imageUrl";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate } from "@tanstack/react-router";
import { X, Trash2, Plus, Minus, ShoppingBag } from "lucide-react";
import { useCartStore } from "@/store/cart";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import logo from "@/assets/parivar-logo.png";

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CartDrawer({ isOpen, onClose }: CartDrawerProps) {
  const { items, addItem, removeItem, updateQuantity, getTotal, clearCart } = useCartStore();
  const navigate = useNavigate();

  const [orderType, setOrderType] = useState<'DINE_IN' | 'TAKE_AWAY'>('DINE_IN');
  const [tableId, setTableId] = useState<string>('');
  const [customerName, setCustomerName] = useState<string>('');
  const [phone, setPhone] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isValidPhone = /^\d{10}$/.test(phone.replace(/\D/g, ''));

  // Fetch tables list from backend public tables endpoint
  const { data: tables } = useQuery({
    queryKey: ["tables-public"],
    queryFn: async () => {
      const res = await fetch((import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/v1/tables");
      return res.json();
    },
    enabled: isOpen,
  });

  // Fetch Add-ons so customers can add extras before placing the order too
  const { data: addons } = useQuery({
    queryKey: ["addons-cart-drawer"],
    queryFn: async () => {
      const res = await fetch((import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/v1/menu?category=" + encodeURIComponent("Add-ons"));
      if (!res.ok) throw new Error("Failed to fetch add-ons");
      const data = await res.json();
      return (data || []).filter((item: any) => item.is_available !== false);
    },
    enabled: isOpen,
  });

  const handlePlaceOrder = async () => {
    setIsSubmitting(true);
    try {
      const payload = orderType === 'DINE_IN'
        ? {
            order_type: 'DINE_IN',
            table_id: parseInt(tableId),
            items: items.map(i => ({ menu_item_id: i.id, quantity: i.quantity, special_notes: i.notes || "" }))
          }
        : {
            order_type: 'TAKE_AWAY',
            customer_name: customerName,
            customer_phone: phone,
            items: items.map(i => ({ menu_item_id: i.id, quantity: i.quantity, special_notes: i.notes || "" }))
          };

      const res = await fetch((import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/v1/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error("Failed to place order");
      }

      const order = await res.json();
      clearCart();
      onClose();
      navigate({ to: `/order-tracking/${order.id}` });
    } catch (err: any) {
      console.error(err);
      alert(err.message || "An error occurred while placing your order.");
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm z-[10000]"
          />
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", bounce: 0, duration: 0.4 }}
            className="fixed top-0 right-0 h-full w-full max-w-md bg-background shadow-2xl z-[10001] flex flex-col"
          >
            <div className="flex items-center justify-between p-6 border-b border-gold/10">
              <h2 className="font-display text-2xl font-semibold flex items-center gap-2 text-foreground">
                <ShoppingBag className="w-6 h-6 text-gold" />
                Your Cart
              </h2>
              <button 
                onClick={onClose}
                className="p-2 rounded-full hover:bg-black/5 transition-colors text-muted-foreground hover:text-foreground"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-4">
              {items.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-muted-foreground gap-4">
                  <ShoppingBag className="w-16 h-16 opacity-20" />
                  <p className="text-lg">Your cart is empty</p>
                  <button 
                    onClick={onClose}
                    className="text-gold font-medium hover:underline"
                  >
                    Continue Browsing
                  </button>
                </div>
              ) : (
                items.map((item) => (
                  <div key={item.id} className="flex gap-4 p-4 rounded-xl border border-gold/10 bg-white/50 backdrop-blur-md relative">
                    {item.image_url && (
                      <div className="w-20 h-20 shrink-0 rounded-lg overflow-hidden">
                        <img
                          src={item.image_url}
                          alt={item.name}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.currentTarget.onerror = null;
                            e.currentTarget.src = logo;
                          }}
                        />
                      </div>
                    )}
                    <div className="flex-1 flex flex-col justify-between">
                      <div className="flex justify-between items-start gap-2">
                        <h3 className="font-medium text-[15px] leading-tight text-foreground">{item.name}</h3>
                        <button 
                          onClick={() => removeItem(item.id)}
                          className="text-red-500/70 hover:text-red-500 transition-colors p-1"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="flex items-center justify-between mt-2">
                        <div className="text-gold font-bold text-lg">${(item.price * item.quantity).toFixed(2)}</div>
                        <div className="flex items-center gap-3 bg-black/5 rounded-full px-2 py-1">
                          <button 
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                            className="w-6 h-6 flex items-center justify-center rounded-full hover:bg-white transition-colors text-foreground"
                          >
                            <Minus className="w-3 h-3" />
                          </button>
                          <span className="font-medium text-sm w-4 text-center text-foreground">{item.quantity}</span>
                          <button 
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                            className="w-6 h-6 flex items-center justify-center rounded-full hover:bg-white transition-colors text-foreground"
                          >
                            <Plus className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}

              {items.length > 0 && addons && addons.length > 0 && (
                <div className="space-y-2">
                  <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Add extras?</h3>
                  {addons.map((addon: any) => (
                    <div key={addon.id ?? addon.name} className="flex items-center gap-3 p-2.5 rounded-lg border border-gold/10 bg-white/40">
                      <div className="w-10 h-10 shrink-0 rounded-md overflow-hidden">
                        <img
                          src={resolveImageUrl(addon.image_url, addon.category?.name, addon.name)}
                          alt={addon.name}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.currentTarget.onerror = null;
                            e.currentTarget.src = logo;
                          }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground truncate">{addon.name}</p>
                        <p className="text-xs text-gold font-semibold">${addon.price.toFixed(2)}</p>
                      </div>
                      <button
                        type="button"
                        onClick={() =>
                          addItem({
                            id: addon.id ? String(addon.id) : addon.name,
                            name: addon.name,
                            price: addon.price,
                            image_url: addon.image_url,
                          })
                        }
                        className="shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-[#0B5D3B] text-cream hover:bg-[#D4A017] transition-colors"
                      >
                        <Plus className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {items.length > 0 && (
                <div className="mt-6 p-4 rounded-xl border border-gold/10 bg-white/30 space-y-4">
                  <h3 className="font-display font-semibold text-lg text-foreground">Order Details</h3>
                  <div>
                    <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Order Type</label>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setOrderType('DINE_IN')}
                        className={`flex-1 py-2 rounded-lg border text-sm font-medium transition-all ${orderType === 'DINE_IN' ? 'bg-[#0B5D3B] text-[#F6E8D7] border-transparent' : 'border-gold/20 text-muted-foreground hover:border-gold/40'}`}
                      >
                        Dine-In
                      </button>
                      <button
                        type="button"
                        onClick={() => setOrderType('TAKE_AWAY')}
                        className={`flex-1 py-2 rounded-lg border text-sm font-medium transition-all ${orderType === 'TAKE_AWAY' ? 'bg-[#0B5D3B] text-[#F6E8D7] border-transparent' : 'border-gold/20 text-muted-foreground hover:border-gold/40'}`}
                      >
                        Take-Away
                      </button>
                    </div>
                  </div>

                  {orderType === 'DINE_IN' ? (
                    <div>
                      <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Select Table</label>
                      <select
                        value={tableId}
                        onChange={(e) => setTableId(e.target.value)}
                        className="w-full px-3 py-2 bg-background border border-gold/20 rounded-lg text-sm text-foreground focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
                      >
                        <option value="">-- Choose a Table --</option>
                        {tables?.map((table: any) => (
                          <option key={table.id} value={table.id} disabled={table.status === 'OCCUPIED'}>
                            Table {table.table_number} ({table.capacity} guests){table.status === 'OCCUPIED' ? ' - Occupied' : ''}
                          </option>
                        ))}
                      </select>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div>
                        <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Name</label>
                        <input
                          type="text"
                          value={customerName}
                          onChange={(e) => setCustomerName(e.target.value)}
                          placeholder="Your Name"
                          className="w-full px-3 py-2 bg-background border border-gold/20 rounded-lg text-sm text-foreground focus:outline-none focus:border-gold"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">Phone Number</label>
                        <input
                          type="tel"
                          value={phone}
                          onChange={(e) => setPhone(e.target.value)}
                          placeholder="Your 10-digit Phone Number"
                          className={`w-full px-3 py-2 bg-background border ${phone && !isValidPhone ? 'border-red-500/50' : 'border-gold/20'} rounded-lg text-sm text-foreground focus:outline-none focus:border-gold`}
                        />
                        {phone && !isValidPhone && <p className="text-[10px] text-red-500 mt-1 text-right">Must be 10 digits</p>}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            {items.length > 0 && (
              <div className="p-6 border-t border-gold/10 bg-white/50 backdrop-blur-md">
                <div className="flex justify-between items-center mb-6 text-xl font-bold text-foreground">
                  <span>Total</span>
                  <span className="text-gold">${getTotal().toFixed(2)}</span>
                </div>
                <button
                  type="button"
                  onClick={handlePlaceOrder}
                  disabled={isSubmitting || (orderType === 'DINE_IN' && !tableId) || (orderType === 'TAKE_AWAY' && (!customerName || !isValidPhone))}
                  className="w-full bg-[#0B5D3B] text-[#F6E8D7] py-4 rounded-xl font-semibold tracking-wide hover:bg-[#D4A017] transition-all duration-300 shadow-md hover:shadow-gold-glow flex justify-center items-center disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? "PLACING ORDER..." : "PLACE ORDER"}
                </button>
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
