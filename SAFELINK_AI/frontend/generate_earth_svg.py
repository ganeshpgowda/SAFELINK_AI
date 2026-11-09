"""Helper script to generate the cyber world map SVG data URI and test it."""
import urllib.parse

# Simplified equirectangular world continent coordinates (1000x500)
# Including Americas, Europe, Africa, Asia, Australia
world_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="1000" height="500">
<defs>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur" />
    <feComposite in="SourceGraphic" in2="blur" operator="over" />
  </filter>
  <pattern id="dotgrid" width="8" height="8" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="0.8" fill="rgba(0,245,160,0.18)"/>
  </pattern>
</defs>

<!-- Subtle Matrix Dots -->
<rect width="1000" height="500" fill="url(#dotgrid)"/>

<!-- Latitude Grid Lines -->
<g stroke="rgba(57,120,214,0.22)" stroke-width="0.75" stroke-dasharray="3,5" fill="none">
  <line x1="0" y1="83" x2="1000" y2="83" />
  <line x1="0" y1="166" x2="1000" y2="166" />
  <line x1="0" y1="250" x2="1000" y2="250" stroke="rgba(0,245,160,0.4)" stroke-dasharray="none" stroke-width="1"/>
  <line x1="0" y1="333" x2="1000" y2="333" />
  <line x1="0" y1="416" x2="1000" y2="416" />
  
  <line x1="166" y1="0" x2="166" y2="500" />
  <line x1="333" y1="0" x2="333" y2="500" />
  <line x1="500" y1="0" x2="500" y2="500" />
  <line x1="666" y1="0" x2="666" y2="500" />
  <line x1="833" y1="0" x2="833" y2="500" />
</g>

<!-- Continents Path in Glowing Cyber Cyan/Mint (#00F5A0) -->
<g fill="rgba(0, 245, 160, 0.45)" stroke="rgba(0, 245, 160, 0.85)" stroke-width="1.2" filter="url(#glow)">
  <!-- North America -->
  <path d="M 65,75 C 90,60 130,50 170,55 C 210,60 250,85 270,110 C 265,145 235,160 205,170 C 195,195 160,215 135,200 C 120,175 105,150 75,125 C 60,110 50,90 65,75 Z" />
  <path d="M 195,175 C 230,175 250,210 240,240 C 220,250 200,240 185,215 Z" />
  <path d="M 215,245 C 235,260 250,270 235,285 C 220,285 205,270 215,245 Z" />
  <!-- Greenland -->
  <path d="M 290,45 C 330,35 365,50 360,80 C 330,95 300,85 290,45 Z" />
  
  <!-- South America -->
  <path d="M 235,275 C 275,270 325,305 330,350 C 320,400 290,445 260,455 C 245,430 250,375 235,335 C 225,305 220,285 235,275 Z" />
  
  <!-- Europe -->
  <path d="M 440,75 C 475,65 520,75 515,115 C 495,145 460,150 440,125 C 430,110 425,90 440,75 Z" />
  <!-- United Kingdom & Scandinavia -->
  <path d="M 415,85 C 430,75 440,90 430,105 C 415,105 410,95 415,85 Z" />
  <path d="M 470,40 C 495,35 505,55 490,75 C 475,75 465,60 470,40 Z" />
  
  <!-- Africa -->
  <path d="M 440,165 C 500,155 565,190 570,250 C 565,310 535,375 490,390 C 465,370 455,320 440,265 C 425,225 425,185 440,165 Z" />
  <path d="M 575,305 C 590,305 595,335 580,350 C 570,340 565,320 575,305 Z" />
  
  <!-- Asia -->
  <path d="M 530,65 C 620,55 750,55 830,85 C 860,115 850,165 800,185 C 750,175 720,215 650,230 C 590,205 560,175 530,125 Z" />
  <!-- India -->
  <path d="M 645,215 C 685,220 690,260 670,295 C 650,295 635,260 645,215 Z" />
  <!-- South East Asia -->
  <path d="M 725,215 C 760,225 765,265 745,285 C 725,275 715,245 725,215 Z" />
  <!-- Japan -->
  <path d="M 835,120 C 855,130 850,165 835,180 C 825,165 825,140 835,120 Z" />
  
  <!-- Australia & Oceania -->
  <path d="M 755,310 C 830,295 865,335 855,385 C 830,410 775,410 750,370 C 740,340 740,320 755,310 Z" />
  <path d="M 875,395 C 890,395 895,425 880,435 C 870,425 865,410 875,395 Z" />
  
  <!-- Antarctica -->
  <path d="M 100,475 C 300,470 700,470 900,475 C 900,490 100,490 100,475 Z" />
</g>

<!-- Cyber Nodes / Active Global Defense Hubs -->
<g fill="#00F5A0" stroke="#FFFFFF" stroke-width="1.5">
  <circle cx="160" cy="120" r="4" />
  <circle cx="270" cy="340" r="3.5" />
  <circle cx="460" cy="105" r="4" />
  <circle cx="510" cy="240" r="4" />
  <circle cx="670" cy="245" r="4" />
  <circle cx="780" cy="150" r="4" />
  <circle cx="800" cy="350" r="4" />
</g>

<!-- Defense Pulse Arcs -->
<g stroke="rgba(57,120,214,0.6)" stroke-width="1.5" fill="none" stroke-dasharray="4,4">
  <path d="M 160,120 Q 310,40 460,105" />
  <path d="M 460,105 Q 620,80 780,150" />
  <path d="M 780,150 Q 790,250 800,350" />
  <path d="M 460,105 Q 480,180 510,240" />
  <path d="M 160,120 Q 200,240 270,340" />
</g>
</svg>"""

encoded_svg = urllib.parse.quote(world_svg)
print("Data URI length:", len(encoded_svg))
with open("frontend/world_map_svg.txt", "w", encoding="utf-8") as f:
    f.write(encoded_svg)
print("Successfully generated world_map_svg.txt")

