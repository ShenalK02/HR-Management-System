/**
 * Birthday Calendar Animation Functions
 * This file contains all animations for the birthday calendar feature
 */

// CONFETTI ANIMATIONS
function playConfettiAnimation(container) {
    // Create confetti elements
    for (let i = 0; i < 100; i++) {
        createConfetti(container);
    }
    
    // Create more confetti every second
    const interval = setInterval(() => {
        for (let i = 0; i < 20; i++) {
            createConfetti(container);
        }
    }, 1000);
    
    // Stop after 10 seconds to avoid performance issues
    setTimeout(() => {
        clearInterval(interval);
    }, 10000);
}

function createConfetti(container) {
    const confetti = document.createElement('div');
    confetti.className = 'confetti';
    
    // Random position, color and size
    confetti.style.left = Math.random() * 100 + '%';
    confetti.style.width = Math.random() * 10 + 5 + 'px';
    confetti.style.height = confetti.style.width;
    
    // Random color
    const colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', 
                    '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50',
                    '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722'];
    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    
    // Random animation duration
    confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
    
    // Add to container
    container.appendChild(confetti);
    
    // Remove after animation completes
    setTimeout(() => {
        if (container.contains(confetti)) {
            container.removeChild(confetti);
        }
    }, 5000);
}

function showConfettiPreview() {
    const previewDiv = document.querySelector('.animation-preview');
    for (let i = 0; i < 30; i++) {
        createConfetti(previewDiv);
    }
}

// BALLOON ANIMATIONS
function playBalloonAnimation(container) {
    // Create balloons
    for (let i = 0; i < 20; i++) {
        createBalloon(container);
    }
    
    // Add a few more every 3 seconds
    const interval = setInterval(() => {
        for (let i = 0; i < 3; i++) {
            createBalloon(container);
        }
    }, 3000);
    
    // Stop after 10 seconds
    setTimeout(() => {
        clearInterval(interval);
    }, 10000);
}

function createBalloon(container) {
    const balloon = document.createElement('div');
    balloon.className = 'balloon';
    
    // Random position
    balloon.style.left = Math.random() * 90 + 5 + '%';
    balloon.style.bottom = -Math.random() * 20 - 50 + 'px';
    
    // Random size
    const size = Math.random() * 30 + 20;
    balloon.style.width = size + 'px';
    balloon.style.height = size * 1.2 + 'px';
    
    // Random color
    const colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', 
                   '#2196f3', '#03a9f4', '#00bcd4', '#4caf50', '#ff9800'];
    balloon.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    
    // String for balloon
    const string = document.createElement('div');
    string.style.position = 'absolute';
    string.style.width = '1px';
    string.style.height = size * 0.9 + 'px';
    string.style.backgroundColor = '#888';
    string.style.bottom = '-' + (size * 0.9) + 'px';
    string.style.left = '50%';
    string.style.transform = 'translateX(-50%)';
    
    balloon.appendChild(string);
    
    // Animation timing
    balloon.style.animationDuration = (Math.random() * 5 + 8) + 's';
    balloon.style.animationDelay = (Math.random() * 3) + 's';
    
    // Add to container
    container.appendChild(balloon);
    
    // Remove after animation completes
    setTimeout(() => {
        if (container.contains(balloon)) {
            container.removeChild(balloon);
        }
    }, 15000);
}

function showBalloonPreview() {
    const previewDiv = document.querySelector('.animation-preview');
    for (let i = 0; i < 8; i++) {
        createBalloon(previewDiv);
    }
}

// FIREWORKS ANIMATIONS
function playFireworksAnimation(container) {
    // Create initial explosion
    createFireworkExplosion(container);
    
    // Create new explosions periodically
    const interval = setInterval(() => {
        createFireworkExplosion(container);
    }, 1200);
    
    // Stop after 10 seconds
    setTimeout(() => {
        clearInterval(interval);
    }, 10000);
}

function createFireworkExplosion(container) {
    // Random position for explosion
    const posX = Math.random() * 80 + 10; // 10-90%
    const posY = Math.random() * 80 + 10; // 10-90%
    
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff8000', '#8000ff'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    // Create particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'firework';
        
        particle.style.left = posX + '%';
        particle.style.top = posY + '%';
        particle.style.backgroundColor = color;
        
        // Random animation duration and delay
        particle.style.animationDuration = (Math.random() * 1 + 1) + 's';
        
        container.appendChild(particle);
        
        // Remove after animation
        setTimeout(() => {
            if (container.contains(particle)) {
                container.removeChild(particle);
            }
        }, 2000);
    }
}

function showFireworksPreview() {
    const previewDiv = document.querySelector('.animation-preview');
    createFireworkExplosion(previewDiv);
    
    // Add a second explosion after a short delay
    setTimeout(() => {
        createFireworkExplosion(previewDiv);
    }, 600);
}

// CAKE ANIMATIONS
function playCakeAnimation(container) {
    // Create cake
    const cakeContainer = document.createElement('div');
    cakeContainer.className = 'cake-container';
    cakeContainer.style.position = 'relative';
    cakeContainer.style.margin = '30px auto';
    cakeContainer.style.width = '100px';
    cakeContainer.style.height = '100px';
    
    const cake = document.createElement('div');
    cake.className = 'cake';
    cakeContainer.appendChild(cake);
    
    // Create candles
    for (let i = 0; i < 3; i++) {
        const candle = document.createElement('div');
        candle.style.position = 'absolute';
        candle.style.width = '5px';
        candle.style.height = '20px';
        candle.style.backgroundColor = '#ffc107';
        candle.style.top = '-20px';
        candle.style.left = (30 + i * 20) + 'px';
        
        const flame = document.createElement('div');
        flame.style.position = 'absolute';
        flame.style.width = '10px';
        flame.style.height = '10px';
        flame.style.backgroundColor = '#ff5722';
        flame.style.borderRadius = '50%';
        flame.style.top = '-10px';
        flame.style.left = '-2.5px';
        flame.style.animation = 'flicker 1s infinite alternate';
        
        candle.appendChild(flame);
        cake.appendChild(candle);
    }
    
    container.appendChild(cakeContainer);
    
    // Add some falling confetti too
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            createConfetti(container);
        }, i * 100);
    }
}

function showCakePreview() {
    const previewDiv = document.querySelector('.animation-preview');
    
    const cake = document.createElement('div');
    cake.className = 'cake';
    cake.style.position = 'relative';
    cake.style.margin = '20px auto';
    
    previewDiv.appendChild(cake);
}

// STARS ANIMATIONS
function playStarsAnimation(container) {
    // Create stars
    for (let i = 0; i < 50; i++) {
        createStar(container);
    }
    
    // Add new stars periodically
    const interval = setInterval(() => {
        for (let i = 0; i < 5; i++) {
            createStar(container);
        }
    }, 2000);
    
    // Stop after 10 seconds
    setTimeout(() => {
        clearInterval(interval);
    }, 10000);
}

function createStar(container) {
    const star = document.createElement('div');
    star.className = 'star';
    
    // Random position
    star.style.left = Math.random() * 95 + '%';
    star.style.top = Math.random() * 95 + '%';
    
    // Random size
    const size = Math.random() * 15 + 5;
    star.style.width = size + 'px';
    star.style.height = size + 'px';
    
    // Random animation duration
    star.style.animationDuration = (Math.random() * 2 + 1) + 's';
    star.style.animationDelay = (Math.random() * 2) + 's';
    
    container.appendChild(star);
    
    // Remove after some time
    setTimeout(() => {
        if (container.contains(star)) {
            container.removeChild(star);
        }
    }, 10000);
}

function showStarsPreview() {
    const previewDiv = document.querySelector('.animation-preview');
    for (let i = 0; i < 15; i++) {
        createStar(previewDiv);
    }
}