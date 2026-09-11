import { motion } from "framer-motion";
import { Heart, Briefcase, Users, Sparkles, Loader2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

const events = [
  { icon: Heart, title: "Weddings", desc: "Regal banquets crafted for your most sacred day." },
  { icon: Briefcase, title: "Corporate Events", desc: "Refined hospitality for boardrooms and galas." },
  { icon: Users, title: "Family Gatherings", desc: "Intimate feasts where every guest feels at home." },
  { icon: Sparkles, title: "Community Events", desc: "Grand spreads for festivals and celebrations." },
];

export function Catering() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [eventType, setEventType] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [guestCount, setGuestCount] = useState("");
  const [requirements, setRequirements] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isValidPhone = /^\d{10}$/.test(phone.replace(/\D/g, ""));
  const canSubmit = name.trim().length > 0 && isValidPhone && !isSubmitting;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setIsSubmitting(true);
    try {
      const res = await fetch((import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/v1/catering/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_name: name,
          phone,
          email: email || undefined,
          event_type: eventType || undefined,
          event_date: eventDate || undefined,
          guest_count: guestCount ? parseInt(guestCount, 10) : undefined,
          requirements: requirements || undefined,
        }),
      });
      if (!res.ok) throw new Error("Failed to submit your request. Please try again.");
      toast.success("Request sent! We'll be in touch shortly to discuss your event.");
      setName("");
      setPhone("");
      setEmail("");
      setEventType("");
      setEventDate("");
      setGuestCount("");
      setRequirements("");
    } catch (err: any) {
      toast.error(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="catering" className="py-32 relative">
      <div className="absolute inset-0 -z-10" style={{
        background: "radial-gradient(ellipse at center, oklch(0.38 0.14 22 / 0.15), transparent 70%)"
      }} />
      <div className="container mx-auto px-6">
        <div className="text-center mb-20">
          <div className="gold-divider justify-center mb-6">
            <span className="h-px w-10 bg-gold/40" /> Bespoke Catering <span className="h-px w-10 bg-gold/40" />
          </div>
          <h2 className="font-display text-5xl md:text-7xl mb-4">
            Bring Parivar to <span className="text-gold-gradient italic">Your Table</span>
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            From intimate gatherings to grand celebrations across Sydney — we bring the kitchen to you.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {events.map((e, i) => (
            <motion.div
              key={e.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className="glass rounded-xl p-8 border-t-2 border-t-gold/40 hover:border-t-gold hover:-translate-y-2 transition-all duration-500"
            >
              <e.icon className="w-9 h-9 text-gold mb-5" strokeWidth={1.2} />
              <h3 className="font-display text-2xl mb-2">{e.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{e.desc}</p>
            </motion.div>
          ))}
        </div>

        <div className="text-center mb-16">
          <a
            href="#catering-form"
            className="inline-flex items-center justify-center px-10 py-4 rounded-full text-sm uppercase tracking-[0.25em] font-medium text-primary-foreground shadow-gold-glow hover:scale-105 transition-transform"
            style={{ background: "var(--gradient-gold)" }}
          >
            Book Catering
          </a>
        </div>

        <motion.form
          id="catering-form"
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="glass rounded-2xl p-8 md:p-10 max-w-2xl mx-auto space-y-5 scroll-mt-32"
        >
          <div className="grid sm:grid-cols-2 gap-5">
            <div>
              <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your Name"
                className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Phone Number</label>
              <input
                type="tel"
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Your 10-digit Phone Number"
                className={`w-full px-4 py-3 bg-background border ${phone && !isValidPhone ? "border-red-500/50" : "border-gold/20"} rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold`}
              />
              {phone && !isValidPhone && <p className="text-[10px] text-red-500 mt-1">Must be 10 digits</p>}
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Email (optional)</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
            />
          </div>

          <div className="grid sm:grid-cols-3 gap-5">
            <div>
              <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Event Type</label>
              <select
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
                className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
              >
                <option value="">-- Select --</option>
                {events.map((ev) => (
                  <option key={ev.title} value={ev.title}>{ev.title}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Event Date</label>
              <input
                type="date"
                value={eventDate}
                onChange={(e) => setEventDate(e.target.value)}
                className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Guest Count</label>
              <input
                type="number"
                min={1}
                value={guestCount}
                onChange={(e) => setGuestCount(e.target.value)}
                placeholder="e.g. 50"
                className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Requirements</label>
            <textarea
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              rows={4}
              placeholder="Tell us about your event, dietary needs, or anything else we should know..."
              className="w-full px-4 py-3 bg-background border border-gold/20 rounded-lg text-sm focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={!canSubmit}
            className="w-full inline-flex items-center justify-center gap-2 px-10 py-4 rounded-full text-sm uppercase tracking-[0.25em] font-medium text-primary-foreground shadow-gold-glow hover:scale-[1.02] transition-transform disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            style={{ background: "var(--gradient-gold)" }}
          >
            {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            {isSubmitting ? "Sending..." : "Submit Request"}
          </button>
        </motion.form>
      </div>
    </section>
  );
}
