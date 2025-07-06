# GitHub Learning Lab Slideshow - API Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Build Scripts API](#build-scripts-api)
3. [Jekyll Configuration](#jekyll-configuration)
4. [Layout Templates](#layout-templates)
5. [Include Components](#include-components)
6. [Content Structure](#content-structure)
7. [Styling System](#styling-system)
8. [JavaScript Integration](#javascript-integration)
9. [Usage Examples](#usage-examples)
10. [Deployment](#deployment)

---

## Project Overview

The GitHub Learning Lab Slideshow is a Jekyll-based presentation system that integrates with reveal.js to create interactive, web-based presentations. It's designed for educational content delivery with features like slide navigation, themes, and responsive design.

### Key Features
- **Jekyll Integration**: Static site generation with Liquid templating
- **Reveal.js Integration**: Interactive presentation framework
- **Responsive Design**: Mobile-friendly presentations
- **Customizable Themes**: Solarized dark/light theme support
- **Font Awesome Icons**: Rich iconography support
- **Automated Deployment**: Scripts for CI/CD workflows

---

## Build Scripts API

### Setup Script (`script/setup`)

**Purpose**: Initializes the development environment with all necessary dependencies.

**Usage**:
```bash
./script/setup
```

**Functions**:
- Installs Homebrew dependencies (macOS only)
- Configures Ruby environment via rbenv
- Installs gem dependencies
- Initializes git submodules

**Example**:
```bash
cd your-slideshow-project
./script/setup
# Output: ==> App is now ready to go!
```

### Development Server (`script/server`)

**Purpose**: Starts a local Jekyll development server.

**Usage**:
```bash
./script/server [jekyll-options]
```

**Parameters**:
- `[jekyll-options]`: Optional Jekyll serve parameters (e.g., `--port 4001`)

**Example**:
```bash
./script/server
# Starts server at http://localhost:4000

./script/server --port 4001
# Starts server at http://localhost:4001
```

### CI Build Script (`script/cibuild`)

**Purpose**: Builds the site for continuous integration environments.

**Usage**:
```bash
./script/cibuild
```

**Functions**:
- Builds Jekyll site with production settings
- Validates HTML using HTMLProofer
- Sets baseurl to "." for relative paths

**Example**:
```bash
./script/cibuild
# Builds site to _site/ directory and validates HTML
```

### Staging Deployment (`script/stage`)

**Purpose**: Deploys the site to a staging environment.

**Usage**:
```bash
./script/stage [repository-name]
```

**Parameters**:
- `[repository-name]`: Optional repository name (defaults to "caption-this")

**Functions**:
- Builds site with staging baseurl
- Creates temporary git repository
- Pushes to staging environment
- Opens staging site in browser

**Example**:
```bash
./script/stage my-presentation
# Deploys to https://pages.ghe.io/training-staging/my-presentation/
```

---

## Jekyll Configuration

### Site Configuration (`_config.yml`)

**Core Settings**:

```yaml
# Basic site information
title: github-slideshow
author: GitHubTeacher
description: A fun activity for learning Git and GitHub.
baseurl: "/github-slideshow"

# Jekyll processing
markdown: kramdown
highlighter: rouge
permalink: "/:title"
```

**Reveal.js Configuration**:

```yaml
reveal:
  controls: false          # Hide navigation controls
  progress: true          # Show progress bar
  history: true           # Enable browser history
  center: true           # Center slides vertically
  transition: linear     # Slide transition effect
  width: 1000           # Presentation width
  height: 920           # Presentation height
```

**Slide Number Configuration**:

```yaml
slideNumber:
  format: "c/t"  # Shows current/total format
  # Options: "h.v", "h/v", "c", "c/t", "none"
```

**Theme Configuration**:

```yaml
solarized:
  theme: dark  # Options: "dark", "light"
```

---

## Layout Templates

### Presentation Layout (`_layouts/presentation.html`)

**Purpose**: Main layout for multi-slide presentations.

**API**:
```html
---
layout: presentation
---
<!-- Your content here -->
```

**Features**:
- Includes reveal.js initialization
- Responsive design
- Theme support
- Script and style loading

**Template Structure**:
```html
<!DOCTYPE html>
<html class="{{theme}}">
<head>
  {% include head.html %}
</head>
<body>
  <div class="reveal">
    <div class="slides">
      {{ content }}
    </div>
  </div>
  {% include script.html %}
</body>
</html>
```

### Slide Layout (`_layouts/slide.html`)

**Purpose**: Layout for individual slide pages.

**API**:
```html
---
layout: slide
title: "Your Slide Title"
---
<!-- Slide content here -->
```

**Usage Example**:
```markdown
---
layout: slide
title: "Welcome to Our Presentation"
---

# Hello World!

This is the content of our slide.

- Bullet point 1
- Bullet point 2
```

---

## Include Components

### Head Component (`_includes/head.html`)

**Purpose**: Manages HTML head section with meta tags, styles, and scripts.

**Features**:
- Responsive meta tags
- Print CSS detection
- Font loading
- jQuery integration

**API Variables**:
- `site.title`: Site title
- `site.author`: Author name
- `site.description`: Site description
- `site.baseurl`: Base URL path

### Script Component (`_includes/script.html`)

**Purpose**: Initializes reveal.js with configuration from `_config.yml`.

**Configuration API**:
```javascript
Reveal.initialize({
  controls: {{ site.reveal.controls }},
  progress: {{ site.reveal.progress }},
  history: {{ site.reveal.history }},
  // ... other options
});
```

**Icon Enhancement**:
```javascript
// Automatically adds icons to external links
$("a.external").append("<i class='fa fa-external-link'></i>");
$("a.twitter").append("<i class='fa fa-twitter'></i>");
$("a.github").append("<i class='fa fa-github'></i>");
```

### Slide Include (`_includes/slide.html`)

**Purpose**: Renders individual slide sections from post content.

**API**:
```html
<section {% if post.slide-id %}id="{{post.slide-id}}"{% endif %} 
         class="step{% for class in post.classes %} {{class}}{% endfor %}">
  {% if post.title != "" %}<h1>{{ post.title }}</h1>{% endif %}
  {{ post.content }}
</section>
```

**Post Variables**:
- `post.slide-id`: Optional slide identifier
- `post.classes`: Array of CSS classes
- `post.title`: Slide title
- `post.content`: Slide content
- `post.data`: Custom data attributes

---

## Content Structure

### Post-based Slides (`_posts/`)

**File Naming Convention**:
```
YYYY-MM-DD-slide-name.md
```

**Front Matter API**:
```yaml
---
layout: slide
title: "Slide Title"
slide-id: "unique-id"          # Optional
classes: ["custom-class"]      # Optional
data:                          # Optional data attributes
  background: "#ff0000"
  transition: "fade"
---
```

**Example Post**:
```markdown
---
layout: slide
title: "Welcome to GitHub"
slide-id: "intro"
classes: ["center", "dark"]
data:
  background: "#24292e"
  transition: "slide"
---

## Getting Started with Git

Learn the fundamentals of version control:

1. **Initialize** your repository
2. **Add** your changes
3. **Commit** your work
4. **Push** to remote

> "Git is a distributed version control system"
```

### Index Page (`index.html`)

**Purpose**: Assembles all posts into a complete presentation.

**API**:
```html
---
layout: presentation
---

{% for post in site.posts reversed %}
  {% include slide.html %}
  <div class="page-break"></div>
{% endfor %}
```

---

## Styling System

### SCSS Architecture

**Main Stylesheet** (`assets/css/style.scss`):
```scss
---
# Jekyll front matter required
---

@import "solarized/solarized.scss";
```

**Mixins** (`_sass/mixin.scss`):
```scss
@mixin border-radius($radius) {
  -webkit-border-radius: $radius;
     -moz-border-radius: $radius;
      -ms-border-radius: $radius;
          border-radius: $radius;
}
```

**Font Configuration** (`_sass/fonts.scss`):
```scss
// Font Awesome integration
// Custom font definitions
```

### Theme System

**Solarized Themes**:
- `solarized/dark.scss`: Dark theme styles
- `solarized/light.scss`: Light theme styles

**Theme Switching**:
```javascript
// Light theme button
$("a.button.lighter").click(function() {
  $("html.dark").removeClass("dark").addClass("light");
});

// Dark theme button
$("a.button.darker").click(function() {
  $("html.light").removeClass("light").addClass("dark");
});
```

---

## JavaScript Integration

### jQuery Integration

**Version**: 1.11.1 (included in `assets/js/`)

**Usage in Templates**:
```html
<script src="{{ site.baseurl }}/assets/js/jquery-1.11.1.min.js"></script>
```

### Reveal.js Configuration

**Dependencies Loading**:
```javascript
dependencies: [
  // Cross-browser classList support
  { 
    src: baseUrl + '/reveal.js/lib/js/classList.js', 
    condition: function() { return !document.body.classList; } 
  },
  
  // Zoom functionality
  { 
    src: baseUrl + '/reveal.js/plugin/zoom-js/zoom.js', 
    async: true 
  },
  
  // Speaker notes
  { 
    src: baseUrl + '/reveal.js/plugin/notes/notes.js', 
    async: true 
  }
]
```

### Custom Event Handlers

**Link Enhancement**:
```javascript
$(document).ready(function() {
  // Add icons to external links
  $("a.external").append("<i class='fa fa-external-link'></i>");
  
  // Add quote icons to blockquotes
  $("blockquote").prepend("<i class='fa fa-quote-left'></i>");
  
  // Theme switching buttons
  $("a.button.lighter").click(function() {
    $("html.dark").removeClass("dark").addClass("light");
  });
});
```

---

## Usage Examples

### Creating a New Slide

1. **Create a new post file**:
```bash
touch _posts/$(date +%Y-%m-%d)-my-new-slide.md
```

2. **Add content**:
```markdown
---
layout: slide
title: "My New Slide"
---

## Slide Content

Your content here...
```

### Adding Custom Styling

1. **Create custom SCSS**:
```scss
// _sass/custom.scss
.my-custom-slide {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  
  h1 {
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }
}
```

2. **Import in main stylesheet**:
```scss
// assets/css/style.scss
---
---
@import "solarized/solarized.scss";
@import "custom";
```

3. **Use in slide**:
```markdown
---
layout: slide
title: "Custom Styled Slide"
classes: ["my-custom-slide"]
---

# Beautiful Slide!
```

### Adding Data Attributes

**For reveal.js features**:
```markdown
---
layout: slide
title: "Animated Slide"
data:
  background-color: "#ff0000"
  background-transition: "slide"
  transition: "zoom"
---

# This slide has custom animations!
```

### Interactive Elements

**Adding navigation hints**:
```markdown
---
layout: slide
title: "Interactive Slide"
---

## Navigation

- Use **←** and **→** arrow keys
- Press **ESC** for overview
- Press **F** for fullscreen

<div class="fragment">
  This text appears on click!
</div>
```

---

## Deployment

### Local Development

```bash
# Setup (one time)
./script/setup

# Start development server
./script/server

# View at http://localhost:4000
```

### Production Build

```bash
# Build for production
./script/cibuild

# Built files in _site/ directory
```

### Staging Deployment

```bash
# Deploy to staging environment
./script/stage my-project-name

# Opens staging URL automatically
```

### GitHub Pages Deployment

**Automatic deployment** when pushing to main branch:

1. **Configure repository settings**
2. **Enable GitHub Pages**
3. **Set source to main branch**
4. **Site available at**: `https://username.github.io/repository-name`

### Custom Domain

**Add CNAME file**:
```bash
echo "your-domain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

---

## Advanced Customization

### Custom Reveal.js Plugins

**Add plugin in `_includes/script.html`**:
```javascript
dependencies: [
  // Existing plugins...
  
  // Custom plugin
  { 
    src: baseUrl + '/assets/js/my-plugin.js', 
    async: true 
  }
]
```

### Custom CSS Classes

**Define in SCSS**:
```scss
.slide.center-image {
  img {
    display: block;
    margin: 0 auto;
    max-width: 80%;
  }
}

.slide.two-column {
  .columns {
    display: flex;
    
    .column {
      flex: 1;
      margin: 0 1rem;
    }
  }
}
```

**Use in slides**:
```markdown
---
layout: slide
title: "Two Column Layout"
classes: ["two-column"]
---

<div class="columns">
  <div class="column">
    ## Left Column
    Content here...
  </div>
  <div class="column">
    ## Right Column
    More content...
  </div>
</div>
```

### Environment Variables

**In `_config.yml`**:
```yaml
# Development settings
development:
  baseurl: ""
  url: "http://localhost:4000"

# Production settings  
production:
  baseurl: "/my-presentation"
  url: "https://mysite.com"
```

**Usage in templates**:
```liquid
{% if jekyll.environment == "production" %}
  <!-- Production only content -->
{% else %}
  <!-- Development only content -->
{% endif %}
```

---

## Troubleshooting

### Common Issues

**1. Ruby Version Conflicts**
```bash
rbenv install 2.7.0
rbenv local 2.7.0
gem install bundler
bundle install
```

**2. Asset Loading Issues**
- Check `baseurl` configuration
- Verify asset paths in templates
- Clear browser cache

**3. Slide Navigation Problems**
- Verify reveal.js configuration
- Check for JavaScript errors
- Ensure proper HTML structure

**4. Styling Issues**
- Check SCSS compilation
- Verify import statements
- Validate CSS syntax

### Debug Mode

**Enable Jekyll debug**:
```bash
JEKYLL_ENV=development bundle exec jekyll serve --verbose
```

**Browser debugging**:
```javascript
// In browser console
console.log(Reveal.getConfig());
console.log(Reveal.getSlides());
```

---

## Contributing

### Code Style

- Use 2 spaces for indentation
- Follow Jekyll conventions
- Comment complex logic
- Use semantic HTML

### Testing

```bash
# Run tests
./script/cibuild

# Validate HTML
bundle exec htmlproofer _site
```

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test locally
5. Submit pull request

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Support

For support and questions:
- Check existing issues
- Create new issue with details
- Include environment information
- Provide minimal reproduction example