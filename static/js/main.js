document.addEventListener('DOMContentLoaded', () => {
    let allItems = [];
    let cart = []; // Array of {id, name, price, quantity}
    let currentCategory = 'All';
    let orderType = 'Dine-In'; // 'Dine-In' or 'Delivery'
    const DELIVERY_FEE = 50.00;

    const menuGrid = document.getElementById('menu-grid');
    const categoryFilters = document.getElementById('category-filters');
    const cartItemsContainer = document.getElementById('cart-items');
    const subtotalEl = document.getElementById('cart-subtotal');
    const taxEl = document.getElementById('cart-tax');
    const deliveryFeeRow = document.getElementById('delivery-fee-row');
    const deliveryFeeEl = document.getElementById('cart-delivery');
    const totalEl = document.getElementById('cart-total');
    const checkoutBtn = document.getElementById('checkout-btn');
    const clearCartBtn = document.getElementById('clear-cart-btn');

    // Toggle Buttons
    const toggleDineIn = document.getElementById('toggle-dinein');
    const toggleDelivery = document.getElementById('toggle-delivery');

    // Payment Modal Elements
    const paymentModal = document.getElementById('payment-modal');
    const modalTotal = document.getElementById('modal-total');
    const paymentLoading = document.getElementById('payment-loading');

    // Emoji mapping for categories for a better look
    const categoryIcons = {
        'Thalis': '👑',
        'Mains': '🍛',
        'Starters': '🥟',
        'Breads': '🫓',
        'South Indian': '🥞',
        'Drinks': '🥤',
        'Desserts': '🍰',
        'Default': '🍽️'
    };

    // Sound effects (optional, graceful fail if audio context blocked)
    const playClickSound = () => {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, ctx.currentTime);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.1);
        } catch(e) {}
    };

    // Fetch Items
    fetch('/api/items')
        .then(res => res.json())
        .then(data => {
            allItems = data;
            renderCategories();
            renderMenu();
        })
        .catch(err => {
            console.error(err);
            showToast('Failed to load menu items', 'error');
        });

    function renderCategories() {
        const categories = ['All', 'Popular', ...new Set(allItems.map(i => i.category))];
        categoryFilters.innerHTML = '';
        
        categories.forEach(cat => {
            const btn = document.createElement('button');
            const isActive = cat === currentCategory;
            
            btn.className = `category-pill whitespace-nowrap px-6 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 border 
                ${isActive ? 'active bg-primary text-white border-primary shadow-md' 
                           : 'bg-white text-muted border-gray-200 hover:border-primary/50 hover:bg-gray-50'}`;
            
            btn.textContent = cat;
            btn.onclick = () => {
                currentCategory = cat;
                renderCategories();
                renderMenu();
            };
            categoryFilters.appendChild(btn);
        });
    }

    let searchQuery = '';
    const menuSearch = document.getElementById('menu-search');
    if (menuSearch) {
        menuSearch.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase();
            renderMenu();
        });
    }

    function renderMenu() {
        if (!menuGrid) return;
        menuGrid.innerHTML = '';
        
        let filtered = allItems;
        if (currentCategory === 'Popular') {
            filtered = [...allItems].sort((a, b) => b.sales_count - a.sales_count).slice(0, 8);
        } else if (currentCategory !== 'All') {
            filtered = allItems.filter(i => i.category === currentCategory);
        }

        if (searchQuery) {
            filtered = filtered.filter(i => i.name.toLowerCase().includes(searchQuery));
        }

        if (filtered.length === 0) {
            menuGrid.innerHTML = `<div class="col-span-full text-center py-10 text-gray-500 font-medium">No items found matching your criteria.</div>`;
            return;
        }

        filtered.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'menu-card bg-white rounded-xl border border-gray-200 cursor-pointer flex flex-col hover:border-primary shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden';
            card.onclick = (e) => {
                // Prevent adding if clicking button directly to avoid double add, handled properly via button click
                addToCart(item);
            };
            
            const slug = item.name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
            let imgPath = `/static/img/${slug}.jpg`;
            if (item.image_url && (item.image_url.startsWith('http://') || item.image_url.startsWith('https://') || item.image_url.startsWith('/static/img/'))) {
                imgPath = item.image_url;
            }
            
            const vegDot = item.is_veg 
                ? `<div class="w-3 h-3 border-2 border-green-600 flex items-center justify-center rounded-sm shrink-0"><div class="w-1.5 h-1.5 bg-green-600 rounded-full"></div></div>`
                : `<div class="w-3 h-3 border-2 border-red-600 flex items-center justify-center rounded-sm shrink-0"><div class="w-1.5 h-1.5 bg-red-600 rounded-full"></div></div>`;
                
            card.innerHTML = `
                <div class="h-32 w-full flex items-center justify-center overflow-hidden bg-primary-soft relative shrink-0">
                    <span class="text-primary text-5xl font-bold absolute">${item.name.charAt(0)}</span>
                    <img src="${imgPath}" alt="${item.name}" class="w-full h-full object-cover relative z-10" onerror="if(this.src !== window.location.origin + '/static/img/${slug}.jpg') { this.src = '/static/img/${slug}.jpg'; } else { this.style.display='none'; }">
                </div>
                <div class="p-3 flex flex-col flex-1 justify-between gap-1">
                    <div class="flex justify-between items-start">
                        <h3 class="font-bold text-text text-sm leading-tight pr-1">${item.name}</h3>
                        <div class="bg-primary-soft text-primary font-bold px-2 py-0.5 rounded-full text-xs shrink-0 whitespace-nowrap">₹${item.price.toFixed(0)}</div>
                    </div>
                    <div class="flex justify-between items-end mt-auto">
                        <div class="flex flex-col gap-1">
                            ${vegDot}
                            <p class="text-[10px] font-semibold text-muted uppercase tracking-wider">${item.category}</p>
                        </div>
                        <button class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center hover:scale-110 transition-transform duration-200 shadow-sm shrink-0">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                        </button>
                    </div>
                </div>
            `;
            menuGrid.appendChild(card);
        });
    }

    const MAX_CART_TOTAL_ITEMS = 20;
    const MAX_ITEM_QUANTITY = 10;

    window.addToCart = function(item) {
        const existing = cart.find(i => i.id === item.id);
        const currentTotal = cart.reduce((sum, i) => sum + i.quantity, 0);
        
        if (currentTotal >= MAX_CART_TOTAL_ITEMS) {
            showToast(`You can only order up to ${MAX_CART_TOTAL_ITEMS} items total!`, 'error');
            return;
        }

        if (existing) {
            if (existing.quantity >= MAX_ITEM_QUANTITY) {
                showToast(`You can only order up to ${MAX_ITEM_QUANTITY} of ${item.name}`, 'error');
                return;
            }
            existing.quantity += 1;
        } else {
            cart.push({ ...item, quantity: 1 });
        }
        showToast(`Added ${item.name} to cart`, 'success');
        updateCart();
        
        playClickSound();
        if(navigator.vibrate) navigator.vibrate(40);
    }

    window.updateQuantity = function(id, delta) {
        const item = cart.find(i => i.id === id);
        if (item) {
            const currentTotal = cart.reduce((sum, i) => sum + i.quantity, 0);
            
            if (delta > 0 && currentTotal >= MAX_CART_TOTAL_ITEMS) {
                showToast(`You can only order up to ${MAX_CART_TOTAL_ITEMS} items total!`, 'error');
                return;
            }
            if (delta > 0 && item.quantity >= MAX_ITEM_QUANTITY) {
                showToast(`You can only order up to ${MAX_ITEM_QUANTITY} of ${item.name}`, 'error');
                return;
            }

            item.quantity += delta;
            if (item.quantity <= 0) {
                cart = cart.filter(i => i.id !== id);
            }
            updateCart();
            playClickSound();
        }
    }

    if(toggleDineIn && toggleDelivery) {
        toggleDineIn.onclick = () => {
            orderType = 'Dine-In';
            toggleDineIn.className = 'flex-1 py-1.5 text-sm font-bold rounded-md bg-primary text-white shadow transition-all';
            toggleDelivery.className = 'flex-1 py-1.5 text-sm font-bold rounded-md text-muted hover:text-text transition-all';
            deliveryFeeRow.classList.add('hidden');
            updateCart();
        };
        toggleDelivery.onclick = () => {
            orderType = 'Delivery';
            toggleDelivery.className = 'flex-1 py-1.5 text-sm font-bold rounded-md bg-primary text-white shadow transition-all';
            toggleDineIn.className = 'flex-1 py-1.5 text-sm font-bold rounded-md text-muted hover:text-text transition-all';
            deliveryFeeRow.classList.remove('hidden');
            updateCart();
        };
    }

    function updateCart() {
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = `
                <div class="text-center text-muted mt-10 flex flex-col items-center gap-3">
                    <svg class="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                    <p class="font-medium text-muted">Your cart is empty</p>
                    <p class="text-sm">Click items from the menu to add them.</p>
                </div>
            `;
            checkoutBtn.disabled = true;
            checkoutBtn.className = 'w-full bg-[#D1D5DB] text-gray-500 font-bold py-4 px-4 rounded-xl shadow-sm transform transition-all cursor-not-allowed flex justify-center items-center gap-2';
            subtotalEl.innerText = "0.00";
            const cgstEl = document.getElementById('cart-cgst');
            const sgstEl = document.getElementById('cart-sgst');
            if (cgstEl) cgstEl.innerText = "0.00";
            if (sgstEl) sgstEl.innerText = "0.00";
            if (taxEl) taxEl.innerText = "0.00";
            totalEl.innerText = "0.00";
            return;
        }

        checkoutBtn.disabled = false;
        checkoutBtn.className = 'w-full bg-primary hover:bg-[#c94d0a] text-white font-bold py-4 px-4 rounded-xl shadow-md transform transition-all hover:scale-105 active:scale-95 flex justify-center items-center gap-2';
        cartItemsContainer.innerHTML = '';
        
        let subtotal = 0;

        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;

            const vegDot = item.is_veg 
                ? `<div class="w-3 h-3 border-2 border-green-600 flex items-center justify-center rounded-sm shrink-0"><div class="w-1.5 h-1.5 bg-green-600 rounded-full"></div></div>`
                : `<div class="w-3 h-3 border-2 border-red-600 flex items-center justify-center rounded-sm shrink-0"><div class="w-1.5 h-1.5 bg-red-600 rounded-full"></div></div>`;
                
            const div = document.createElement('div');
            div.className = 'flex justify-between items-center p-3 bg-white border border-gray-200 rounded-xl shadow-sm animate-[fadeIn_0.2s_ease-out] hover:border-primary transition-colors';
            div.innerHTML = `
                <div class="flex-1 min-w-0 pr-2">
                    <div class="flex items-center gap-2 mb-1">
                        ${vegDot}
                        <h4 class="text-sm font-bold text-text truncate">${item.name}</h4>
                    </div>
                    <div class="text-xs text-primary font-bold">₹${item.price.toFixed(2)}</div>
                </div>
                <div class="flex flex-col items-end gap-2">
                    <div class="flex items-center space-x-3">
                        <div class="flex items-center bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                            <button onclick="updateQuantity(${item.id}, -1)" class="w-7 h-7 flex items-center justify-center text-muted hover:bg-gray-200 hover:text-primary transition-colors font-bold text-lg leading-none">-</button>
                            <span class="w-6 text-center text-sm font-bold text-text">${item.quantity}</span>
                            <button onclick="updateQuantity(${item.id}, 1)" class="w-7 h-7 flex items-center justify-center text-muted hover:bg-gray-200 hover:text-primary transition-colors font-bold text-lg leading-none">+</button>
                        </div>
                        <div class="w-14 text-right font-bold text-text text-sm">
                            ₹${itemTotal.toFixed(2)}
                        </div>
                    </div>
                    <button onclick="updateQuantity(${item.id}, -${item.quantity})" class="text-xs text-danger hover:text-red-700 flex items-center gap-1">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        Remove
                    </button>
                </div>
            `;
            cartItemsContainer.appendChild(div);
        });

        const tax = subtotal * 0.05;
        const halfTax = tax / 2;
        let fee = orderType === 'Delivery' ? DELIVERY_FEE : 0;
        const total = subtotal + tax + fee;

        subtotalEl.innerText = subtotal.toFixed(2);
        const cgstEl = document.getElementById('cart-cgst');
        const sgstEl = document.getElementById('cart-sgst');
        if (cgstEl) cgstEl.innerText = halfTax.toFixed(2);
        if (sgstEl) sgstEl.innerText = halfTax.toFixed(2);
        
        if (taxEl) taxEl.innerText = tax.toFixed(2);
        totalEl.innerText = total.toFixed(2);
        
        // Update modal total as well
        if (modalTotal) modalTotal.innerText = total.toFixed(2);
    }

    if(clearCartBtn) {
        clearCartBtn.onclick = () => {
            if(confirm("Are you sure you want to clear the entire order?")) {
                cart = [];
                updateCart();
                showToast("Cart cleared", "success");
            }
        };
    }

    let selectedTable = null;
    let occupiedTables = [];

    // Modal Logic
    if(checkoutBtn) {
        checkoutBtn.onclick = () => {
            if (cart.length === 0) return;
            
            const dynamicFields = document.getElementById('modal-dynamic-fields');
            dynamicFields.innerHTML = '';
            
            if (orderType === 'Dine-In') {
                dynamicFields.innerHTML = `
                    <div class="space-y-3 animate-[fadeIn_0.2s_ease-out]">
                        <input type="text" id="customer-name" placeholder="Customer Name (Optional)" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors">
                        <div>
                            <div class="relative">
                                <input type="tel" id="customer-phone" maxlength="10" placeholder="Phone Number (Optional - 10 digits)" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" oninput="validateCheckoutPhone(this, false)" onblur="validateCheckoutPhone(this, false)">
                                <span id="checkout-phone-count" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-medium text-muted pointer-events-none">0/10</span>
                            </div>
                            <p id="checkout-phone-err" class="text-xs text-red-500 mt-1 hidden"></p>
                        </div>
                        <div id="table-picker-container"></div>
                        <textarea id="order-note" placeholder="Optional Note" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" rows="1"></textarea>
                    </div>
                `;
                // Fetch occupied tables (optional, can be cached)
                fetch('/api/tables').then(r=>r.json()).then(data => {
                    occupiedTables = data.occupied || [];
                    renderTablePicker();
                }).catch(() => {
                    renderTablePicker();
                });
            } else {
                dynamicFields.innerHTML = `
                    <div class="space-y-3 animate-[fadeIn_0.2s_ease-out]">
                        <input type="text" id="customer-name" placeholder="Customer Name *" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" required>
                        <div>
                            <div class="relative">
                                <input type="tel" id="customer-phone" maxlength="10" placeholder="Phone Number (10 digits) *" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" required oninput="validateCheckoutPhone(this, true)" onblur="validateCheckoutPhone(this, true)">
                                <span id="checkout-phone-count" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-medium text-muted pointer-events-none">0/10</span>
                            </div>
                            <p id="checkout-phone-err" class="text-xs text-red-500 mt-1 hidden"></p>
                        </div>
                        <textarea id="customer-address" placeholder="Delivery Address *" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" rows="2" required></textarea>
                        <textarea id="order-note" placeholder="Optional Note" class="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-text focus:outline-none focus:border-primary transition-colors" rows="1"></textarea>
                    </div>
                `;
            }
            
            paymentModal.classList.remove('hidden');
        };
    }
    
    function renderTablePicker() {
        const container = document.getElementById('table-picker-container');
        if (!container) return;
        
        let gridHtml = '<div class="grid grid-cols-5 gap-2 animate-[fadeIn_0.2s_ease-out]">';
        for (let i = 1; i <= 10; i++) {
            const t = 'T' + i;
            const isOccupied = occupiedTables.includes(t);
            const isSelected = selectedTable === t;
            let btnClass = 'py-2 rounded-lg font-bold text-center border transition-all cursor-pointer text-sm ';
            
            if (isOccupied) {
                btnClass += 'bg-danger/10 border-danger/30 text-danger opacity-70 cursor-not-allowed';
            } else if (isSelected) {
                btnClass += 'bg-primary text-white border-primary shadow-md';
            } else {
                btnClass += 'bg-gray-50 border-gray-200 text-text hover:border-primary/50 hover:bg-primary-soft';
            }
            
            gridHtml += `<div onclick="if(!${isOccupied}) { window.selectTable('${t}'); }" class="${btnClass}">${t}</div>`;
        }
        gridHtml += '</div>';
        container.innerHTML = gridHtml;
    }
    
    window.selectTable = function(t) {
        selectedTable = t;
        renderTablePicker();
    }

    window.closePaymentModal = function() {
        paymentModal.classList.add('hidden');
        selectedTable = null;
        if(window.hideCashCalculator) window.hideCashCalculator();
    }

    window.setExactCash = () => {
        let subtotal = Object.values(cart).reduce((sum, item) => sum + (item.price * item.quantity), 0);
        let tax = subtotal * 0.05;
        let fee = orderType === 'Delivery' ? DELIVERY_FEE : 0;
        let total = subtotal + tax + fee;
        const cashInput = document.getElementById('cash-received');
        if (cashInput) {
            cashInput.value = total.toFixed(2);
            window.calculateChange();
        }
    };

    window.setQuickCash = (amt) => {
        const cashInput = document.getElementById('cash-received');
        if (cashInput) {
            cashInput.value = Number(amt).toFixed(2);
            window.calculateChange();
        }
    };

    window.showCashCalculator = () => {
        document.getElementById('payment-options').classList.add('hidden');
        document.getElementById('cash-calculator').classList.remove('hidden');
        
        let subtotal = Object.values(cart).reduce((sum, item) => sum + (item.price * item.quantity), 0);
        let tax = subtotal * 0.05;
        let fee = orderType === 'Delivery' ? DELIVERY_FEE : 0;
        let total = subtotal + tax + fee;

        const cashInput = document.getElementById('cash-received');
        // Auto-fill exact bill amount so cashier doesn't need to retype
        cashInput.value = total.toFixed(2);

        // Populate quick cash suggestion chips
        const quickContainer = document.getElementById('quick-cash-container');
        if (quickContainer) {
            quickContainer.innerHTML = '';
            const suggestions = [];
            suggestions.push({ label: `Exact (₹${total.toFixed(2)})`, value: total.toFixed(2) });

            const ceil50 = Math.ceil(total / 50) * 50;
            const ceil100 = Math.ceil(total / 100) * 100;
            const ceil500 = Math.ceil(total / 500) * 500;

            if (ceil50 > total && !suggestions.some(s => s.value == ceil50)) {
                suggestions.push({ label: `₹${ceil50}`, value: ceil50 });
            }
            if (ceil100 > total && !suggestions.some(s => s.value == ceil100)) {
                suggestions.push({ label: `₹${ceil100}`, value: ceil100 });
            }
            if (ceil500 > total && !suggestions.some(s => s.value == ceil500)) {
                suggestions.push({ label: `₹${ceil500}`, value: ceil500 });
            }
            if (total < 2000 && !suggestions.some(s => s.value == 2000)) {
                suggestions.push({ label: `₹2000`, value: 2000 });
            }

            suggestions.slice(0, 4).forEach(item => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'px-2.5 py-1 text-xs font-bold rounded-lg border border-gray-200 bg-white hover:border-primary hover:bg-primary-soft text-text transition-colors';
                btn.innerText = item.label;
                btn.onclick = () => window.setQuickCash(item.value);
                quickContainer.appendChild(btn);
            });
        }

        window.calculateChange();

        // Listen for Enter key to immediately submit
        cashInput.onkeydown = (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const confirmBtn = document.getElementById('confirm-cash-btn');
                if (confirmBtn && !confirmBtn.disabled) {
                    window.processPayment('Cash');
                }
            }
        };

        setTimeout(() => {
            cashInput.focus();
            cashInput.select();
        }, 100);
    };

    window.hideCashCalculator = () => {
        const opts = document.getElementById('payment-options');
        const calc = document.getElementById('cash-calculator');
        if(opts) opts.classList.remove('hidden');
        if(calc) calc.classList.add('hidden');
    };

    window.calculateChange = () => {
        const receivedStr = document.getElementById('cash-received').value;
        const received = parseFloat(receivedStr) || 0;
        
        let subtotal = Object.values(cart).reduce((sum, item) => sum + (item.price * item.quantity), 0);
        let tax = subtotal * 0.05;
        let fee = orderType === 'Delivery' ? DELIVERY_FEE : 0;
        let total = subtotal + tax + fee;

        const change = received - total;
        const changeEl = document.getElementById('cash-change');
        const btn = document.getElementById('confirm-cash-btn');

        // Allow 1 cent margin for float rounding
        if (received >= total - 0.01) {
            const displayChange = Math.max(0, change);
            changeEl.innerText = '₹' + displayChange.toFixed(2);
            changeEl.className = 'text-xl font-extrabold text-green-600';
            btn.disabled = false;
        } else {
            changeEl.innerText = 'Insufficient';
            changeEl.className = 'text-xl font-extrabold text-red-500';
            btn.disabled = true;
        }
    };

    window.validateCheckoutPhone = function(input, isRequired = false) {
        input.value = input.value.replace(/\D/g, '').slice(0, 10);
        const err = document.getElementById('checkout-phone-err');
        const count = document.getElementById('checkout-phone-count');
        const val = input.value;
        const len = val.length;

        if (count) {
            count.innerText = `${len}/10`;
            if (len === 10) count.className = 'absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-bold text-emerald-600 pointer-events-none';
            else if (len > 0) count.className = 'absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-medium text-amber-600 pointer-events-none';
            else count.className = 'absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-medium text-muted pointer-events-none';
        }

        if (len === 0) {
            if (isRequired) {
                input.classList.remove('border-gray-300');
                input.classList.add('border-red-500');
                if (err) {
                    err.innerText = 'Phone number is required (10 digits)';
                    err.classList.remove('hidden');
                }
                return false;
            } else {
                input.classList.remove('border-red-500');
                input.classList.add('border-gray-300');
                if (err) err.classList.add('hidden');
                return true;
            }
        }

        if (len < 10) {
            input.classList.remove('border-gray-300');
            input.classList.add('border-red-500');
            if (err) {
                err.innerText = `Must be exactly 10 digits (${len}/10 entered)`;
                err.classList.remove('hidden');
            }
            return false;
        }

        input.classList.remove('border-red-500');
        input.classList.add('border-gray-300');
        if (err) err.classList.add('hidden');
        return true;
    };

    let isProcessingOrder = false;

    window.processPayment = function(method) {
        if (isProcessingOrder) return; // Prevent double click or duplicate submissions

        if (cart.length === 0) {
            showToast('Your cart is empty', 'error');
            return;
        }

        const customerName = document.getElementById('customer-name')?.value || '';
        const customerPhone = document.getElementById('customer-phone')?.value || '';
        const customerAddress = document.getElementById('customer-address')?.value || '';
        const orderNote = document.getElementById('order-note')?.value || '';

        if (orderType === 'Delivery') {
            if (!customerName.trim() || !customerPhone.trim() || !customerAddress.trim()) {
                showToast('Please fill all required delivery fields', 'error');
                return;
            }
            if (!/^\d{10}$/.test(customerPhone.trim())) {
                showToast('Phone number must be exactly 10 digits', 'error');
                const pEl = document.getElementById('customer-phone');
                if (pEl) { pEl.focus(); validateCheckoutPhone(pEl, true); }
                return;
            }
        } else {
            if (customerPhone.trim() && !/^\d{10}$/.test(customerPhone.trim())) {
                showToast('Phone number must be exactly 10 digits', 'error');
                const pEl = document.getElementById('customer-phone');
                if (pEl) { pEl.focus(); validateCheckoutPhone(pEl, false); }
                return;
            }
            if (!selectedTable) {
                showToast('Please select a table', 'error');
                return;
            }
        }

        isProcessingOrder = true;
        paymentLoading.classList.remove('hidden');
        
        const confirmBtn = document.getElementById('confirm-cash-btn');
        if (confirmBtn) {
            confirmBtn.disabled = true;
            confirmBtn.innerText = 'Processing...';
        }

        const payload = {
            items: cart.map(i => ({ id: i.id, quantity: i.quantity })),
            order_type: orderType,
            delivery_fee: orderType === 'Delivery' ? DELIVERY_FEE : 0,
            customer_name: customerName.trim(),
            customer_phone: customerPhone.trim(),
            customer_address: customerAddress.trim(),
            table_number: orderType === 'Dine-In' ? selectedTable : null,
            order_note: orderNote.trim(),
            payment_mode: method
        };

        fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(errData => {
                    throw new Error(errData.error || 'Server error occurred');
                });
            }
            return res.json();
        })
        .then(data => {
            paymentLoading.classList.add('hidden');
            paymentModal.classList.add('hidden');
            selectedTable = null;
            if (window.hideCashCalculator) window.hideCashCalculator();

            showToast('Payment Successful & Order Generated!');

            try {
                // Live update sidebar sales
                const salesEl = document.getElementById('sidebar-daily-sales');
                if (salesEl) {
                    const current = parseFloat(salesEl.innerText) || 0;
                    salesEl.innerText = (current + data.total).toFixed(2);
                }
                cart = [];
                updateCart();
            } catch (cleanupErr) {
                console.warn('Post-checkout UI cleanup error:', cleanupErr);
            }
            setTimeout(() => {
                window.location.href = `/receipt/${data.bill_number}`;
            }, 300);
        })
        .catch(err => {
            console.error('Payment error:', err);
            isProcessingOrder = false;
            paymentLoading.classList.add('hidden');
            if (confirmBtn) {
                confirmBtn.disabled = false;
                confirmBtn.innerText = 'Confirm Payment';
            }
            showToast(err.message || 'Payment failed', 'error');
        });
    }
});