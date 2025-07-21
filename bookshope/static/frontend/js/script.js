// DOM Elements
const loginBtn = document.getElementById("loginBtn")
const loginModal = document.getElementById("loginModal")
const closeModal = document.querySelector(".close")
const authTabs = document.querySelectorAll(".auth-tab")
const loginForm = document.getElementById("loginForm")
const registerForm = document.getElementById("registerForm")
const addToCartBtns = document.querySelectorAll(".add-to-cart")
const cartCount = document.querySelector(".cart-count")
const searchInput = document.querySelector(".search-input")
const newsletterForm = document.querySelector(".newsletter-form")

// Cart functionality
const cart = []

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initializeAnimations()
  initializeNavbar()
  initializeModal()
  initializeCart()
  initializeSearch()
  initializeNewsletter()
})

// Navbar scroll effect
function initializeNavbar() {
  const navbar = document.querySelector(".navbar")

  window.addEventListener("scroll", () => {
    var themeValue = localStorage.getItem('theme')
    if (themeValue === 'dark') {
      if (window.scrollY > 100) {
      navbar.style.background = "rgba(26, 26, 26, 0.98)"
      navbar.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.3)"
      } else {
        navbar.style.background = "rgba(26, 26, 26, 0.95)"
        navbar.style.boxShadow = "none"
      }
    }
    else{
      if (window.scrollY > 100) {
        navbar.style.background = "rgba(212, 242, 249, 0.98)"
        navbar.style.boxShadow = "0 4px 20px rgba(152, 207, 219, 0.98)"
      } else {
        navbar.style.background = "rgba(208, 242, 250, 0.98)"
        navbar.style.boxShadow = "none"
      }
    }
  })

  // Smooth scroll for navigation links
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]')
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      const targetId = link.getAttribute("href")
      const targetSection = document.querySelector(targetId)

      if (targetSection) {
        targetSection.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
}

// Modal functionality
function initializeModal() {
  // Open modal
  // loginBtn.addEventListener("click", (e) => {
  //   e.preventDefault()
  //   loginModal.style.display = "block"
  //   document.body.style.overflow = "hidden"
  // })

  // Close modal
  closeModal.addEventListener("click", () => {
    loginModal.style.display = "none"
    document.body.style.overflow = "auto"
  })

  // Close modal when clicking outside
  // window.addEventListener("click", (e) => {
  //   if (e.target === loginModal) {
  //     loginModal.style.display = "none"
  //     document.body.style.overflow = "auto"
  //   }
  // })

  // Tab switching
  authTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const tabType = tab.getAttribute("data-tab")

      // Remove active class from all tabs
      authTabs.forEach((t) => t.classList.remove("active"))
      tab.classList.add("active")

      // Show/hide forms
      if (tabType === "login") {
        loginForm.style.display = "block"
        registerForm.style.display = "none"
      } else {
        loginForm.style.display = "none"
        registerForm.style.display = "block"
      }
    })
  })
}

// Cart functionality
function initializeCart() {
  addToCartBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault()
      addToCart()

      // Add animation feedback
      btn.style.transform = "scale(0.95)"
      btn.textContent = "Added!"
      btn.style.background = "#4CAF50"

      setTimeout(() => {
        btn.style.transform = "scale(1)"
        btn.textContent = "Add to Cart"
        btn.style.background = ""
      }, 1000)
    })
  })
}

function addToCart() {
  cart.push({
    id: Date.now(),
    title: "Sample Book",
    price: 24.99,
  })

  updateCartCount()
  showNotification("Book added to cart!")
}

function updateCartCount() {
  cartCount.textContent = cart.length

  // Add bounce animation
  cartCount.style.animation = "none"
  setTimeout(() => {
    cartCount.style.animation = "bounce 0.5s ease-out"
  }, 10)
}

// Search functionality
// function initializeSearch() {
//   let searchTimeout

//   searchInput.addEventListener("input", (e) => {
//     clearTimeout(searchTimeout)
//     const query = e.target.value.trim()

//     if (query.length > 2) {
//       searchTimeout = setTimeout(() => {
//         performSearch(query)
//       }, 300)
//     }
//   })

//   searchInput.addEventListener("keypress", (e) => {
//     if (e.key === "Enter") {
//       e.preventDefault()
//       const query = e.target.value.trim()
//       if (query) {
//         performSearch(query)
//       }
//     }
//   })
// }

// function performSearch(query) {
//   // Simulate search functionality
//   console.log(`Searching for: ${query}`)
//   showNotification(`Searching for "${query}"...`)

//   // Add search animation
//   const searchIcon = document.querySelector(".search-icon")
//   searchIcon.style.animation = "spin 1s linear"

//   setTimeout(() => {
//     searchIcon.style.animation = ""
//     showNotification(`Found results for "${query}"`)
//   }, 1000)
// }

// Newsletter functionality
// function initializeNewsletter() {
//   newsletterForm.addEventListener("submit", (e) => {
//     e.preventDefault()
//     const email = e.target.querySelector('input[type="email"]').value

//     if (email) {
//       // Simulate newsletter signup
//       const button = e.target.querySelector("button")
//       const originalText = button.textContent

//       button.textContent = "Subscribing..."
//       button.disabled = true

//       setTimeout(() => {
//         button.textContent = "Subscribed!"
//         button.style.background = "#4CAF50"
//         showNotification("Successfully subscribed to newsletter!")

//         setTimeout(() => {
//           button.textContent = originalText
//           button.disabled = false
//           button.style.background = ""
//           e.target.reset()
//         }, 2000)
//       }, 1500)
//     }
//   })
// }

// Animations
function initializeAnimations() {
  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = "fadeInUp 0.8s ease-out forwards"
      }
    })
  }, observerOptions)

  // Observe elements for animation
  const animateElements = document.querySelectorAll(".author-card, .book-card, .premium-text, .newsletter-content")
  animateElements.forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(30px)"
    observer.observe(el)
  })

  // Parallax effect for hero section
  window.addEventListener("scroll", () => {
    const scrolled = window.pageYOffset
    const parallaxElements = document.querySelectorAll(".floating-books")

    parallaxElements.forEach((el) => {
      const speed = 0.5
      el.style.transform = `translateY(${scrolled * speed}px)`
    })
  })
}

// Utility functions
function showNotification(message) {
  // Create notification element
  const notification = document.createElement("div")
  notification.className = "notification"
  notification.textContent = message
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--accent-color);
        color: var(--primary-color);
        padding: 15px 20px;
        border-radius: 8px;
        font-weight: 600;
        z-index: 3000;
        animation: slideInRight 0.3s ease-out;
        box-shadow: var(--shadow-dark);
    `

  document.body.appendChild(notification)

  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.style.animation = "slideOutRight 0.3s ease-out"
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}

// Add notification animations to CSS
const notificationStyles = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
`

// Inject notification styles
const styleSheet = document.createElement("style")
styleSheet.textContent = notificationStyles
document.head.appendChild(styleSheet)

// Mobile menu functionality
const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
const navMenuElement = document.querySelector(".nav-menu")

if (mobileMenuToggle && navMenuElement) {
  mobileMenuToggle.addEventListener("click", () => {
    navMenuElement.classList.toggle("active")
    mobileMenuToggle.classList.toggle("active")
  })
}

// Book hover effects
document.querySelectorAll(".book-card").forEach((card) => {
  card.addEventListener("mouseenter", () => {
    card.style.transform = "translateY(-10px) scale(1.02)"
  })

  card.addEventListener("mouseleave", () => {
    card.style.transform = "translateY(0) scale(1)"
  })
})

// Smooth page loading
window.addEventListener("load", () => {
  document.body.style.opacity = "0"
  document.body.style.transition = "opacity 0.5s ease-in-out"

  setTimeout(() => {
    document.body.style.opacity = "1"
  }, 100)
})

// Category dropdown functionality
const categoryDropdown = document.querySelector(".category-dropdown")
const megaMenu = document.querySelector(".mega-menu")

if (categoryDropdown && megaMenu) {
  let hoverTimeout

  categoryDropdown.addEventListener("mouseenter", () => {
    clearTimeout(hoverTimeout)
    megaMenu.style.opacity = "1"
    megaMenu.style.visibility = "visible"
    megaMenu.style.transform = "translateY(0)"
  })

  categoryDropdown.addEventListener("mouseleave", () => {
    hoverTimeout = setTimeout(() => {
      megaMenu.style.opacity = "0"
      megaMenu.style.visibility = "hidden"
      megaMenu.style.transform = "translateY(-10px)"
    }, 200)
  })
}

// Add loading states for buttons
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", function () {
    if (!this.disabled) {
      this.style.transform = "scale(0.98)"
      setTimeout(() => {
        this.style.transform = "scale(1)"
      }, 150)
    }
  })
})

// Performance optimization: Lazy loading for images
const images = document.querySelectorAll("img")
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const img = entry.target
      if (img.dataset.src) {
        img.src = img.dataset.src
        img.removeAttribute("data-src")
      }
      imageObserver.unobserve(img)
    }
  })
})

images.forEach((img) => {
  imageObserver.observe(img)
})

// Add ripple effect to buttons
function createRipple(event) {
  const button = event.currentTarget
  const circle = document.createElement("span")
  const diameter = Math.max(button.clientWidth, button.clientHeight)
  const radius = diameter / 2

  circle.style.width = circle.style.height = `${diameter}px`
  circle.style.left = `${event.clientX - button.offsetLeft - radius}px`
  circle.style.top = `${event.clientY - button.offsetTop - radius}px`
  circle.classList.add("ripple")

  const ripple = button.getElementsByClassName("ripple")[0]
  if (ripple) {
    ripple.remove()
  }

  button.appendChild(circle)
}

// Add ripple styles
const rippleStyles = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 600ms linear;
        background-color: rgba(255, 255, 255, 0.6);
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    button {
        position: relative;
        overflow: hidden;
    }
`

const rippleStyleSheet = document.createElement("style")
rippleStyleSheet.textContent = rippleStyles
document.head.appendChild(rippleStyleSheet)

// Apply ripple effect to all buttons
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", createRipple)
})

// Enhanced scroll to top functionality
const scrollToTopBtn = document.createElement("button")
scrollToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>'
scrollToTopBtn.className = "scroll-to-top"
scrollToTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background: var(--gradient-gold);
    color: var(--primary-color);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: var(--transition);
    z-index: 1000;
    box-shadow: var(--shadow-dark);
`

document.body.appendChild(scrollToTopBtn)

window.addEventListener("scroll", () => {
  if (window.pageYOffset > 300) {
    scrollToTopBtn.style.opacity = "1"
    scrollToTopBtn.style.visibility = "visible"
  } else {
    scrollToTopBtn.style.opacity = "0"
    scrollToTopBtn.style.visibility = "hidden"
  }
})

scrollToTopBtn.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  })
})

// Theme persistence
// const themeToggle = document.createElement("button")
// themeToggle.innerHTML = '<i class="fas fa-moon"></i>'
// themeToggle.className = "theme-toggle"
// themeToggle.style.cssText = `
//     position: fixed;
//     bottom: 90px;
//     right: 30px;
//     width: 50px;
//     height: 50px;
//     background: var(--secondary-color);
//     color: var(--text-primary);
//     border: 1px solid var(--accent-color);
//     border-radius: 50%;
//     cursor: pointer;
//     transition: var(--transition);
//     z-index: 1000;
// `

const themeToggle = document.createElement("button");
  themeToggle.innerHTML = '<i class="fas fa-moon"></i>'; // default icon
  themeToggle.className = "theme-toggle";
  themeToggle.style.cssText = `
    position: fixed;
    bottom: 90px;
    right: 30px;
    width: 50px;
    height: 50px;
    background: var(--secondary-color);
    color: var(--text-primary);
    border: 1px solid var(--accent-color);
    border-radius: 50%;
    cursor: pointer;
    transition: var(--transition);
    z-index: 1000;
  `;
  document.body.appendChild(themeToggle);

  // Function to apply theme from storage
  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.classList.add("light-theme");
      themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
      document.documentElement.classList.remove("light-theme");
      themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
  }

  // Load theme on page load
  const savedTheme = localStorage.getItem("theme") || "dark";
  applyTheme(savedTheme);

  // Toggle on click
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.classList.contains("light-theme") ? "light" : "dark";
    const newTheme = currentTheme === "light" ? "dark" : "light";
    applyTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  });


  
document.body.appendChild(themeToggle)

// Error handling for failed image loads
images.forEach((img) => {
  img.addEventListener("error", function () {
    this.alt = "Image not available"
  })
})

console.log("LuxeBooks - Premium Bookshop Initialized Successfully")



// <!-- JS (Attach to existing JS file or inline for demo) -->
// <script>
  // Mobile Menu Toggle
  document.querySelector(".mobile-menu-toggle").addEventListener("click", () => {
    document.querySelector(".nav-menu").classList.toggle("active")
  })

  // Open Cart Sidebar
  document.querySelector(".cart-icon").addEventListener("click", () => {
    document.querySelector(".cart-sidebar").classList.add("open")
  })

  // Close Cart Sidebar
  document.querySelector(".close-cart").addEventListener("click", () => {
    document.querySelector(".cart-sidebar").classList.remove("open")
  })

  

setTimeout(() => {
  document.querySelectorAll('.message').forEach(el => el.style.display = 'none');
}, 5000);
  