(function () {
  "use strict";

  const content = document.querySelector("[data-page-content]");
  const toc = document.querySelector("[data-toc]");
  const tocNav = document.querySelector("[data-toc-nav]");

  if (!content || !toc || !tocNav) return;

  const headings = Array.from(content.querySelectorAll("h2, h3"));
  if (!headings.length) return;

  const usedIds = new Set(
    Array.from(document.querySelectorAll("[id]"))
      .map((element) => element.id)
      .filter(Boolean)
  );

  function slugify(value) {
    const base = value
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-") || "section";

    let slug = base;
    let suffix = 2;
    while (usedIds.has(slug)) {
      slug = `${base}-${suffix}`;
      suffix += 1;
    }

    usedIds.add(slug);
    return slug;
  }

  const rootList = document.createElement("ol");
  rootList.className = "toc-list";
  let currentSection = null;
  const links = new Map();

  headings.forEach((heading) => {
    if (!heading.id) heading.id = slugify(heading.textContent);

    const title = heading.textContent.trim();
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = `#${encodeURIComponent(heading.id)}`;
    link.textContent = title;
    item.appendChild(link);
    links.set(heading.id, link);

    if (heading.tagName === "H2") {
      item.className = "toc-item toc-item-h2";
      rootList.appendChild(item);
      currentSection = item;
    } else {
      item.className = "toc-item toc-item-h3";
      let childList = currentSection && currentSection.querySelector(":scope > .toc-sublist");
      if (!childList) {
        childList = document.createElement("ol");
        childList.className = "toc-sublist";
        (currentSection || rootList).appendChild(childList);
      }
      childList.appendChild(item);
    }

    const anchor = document.createElement("a");
    anchor.className = "heading-anchor";
    anchor.href = `#${encodeURIComponent(heading.id)}`;
    anchor.setAttribute("aria-label", `Link to ${title}`);
    anchor.textContent = "#";
    heading.appendChild(anchor);
  });

  tocNav.appendChild(rootList);
  toc.hidden = false;

  let scheduled = false;
  function setActiveLink() {
    const threshold = Math.min(window.innerHeight * 0.25, 180);
    let activeHeading = headings[0];

    for (const heading of headings) {
      if (heading.getBoundingClientRect().top <= threshold) activeHeading = heading;
      else break;
    }

    const pageBottom = window.scrollY + window.innerHeight;
    const documentBottom = document.documentElement.scrollHeight;
    if (pageBottom >= documentBottom - 4) {
      activeHeading = headings[headings.length - 1];
    }

    links.forEach((link, id) => {
      const isActive = id === activeHeading.id;
      link.classList.toggle("is-active", isActive);
      if (isActive) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });

    scheduled = false;
  }

  function scheduleActiveLink() {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(setActiveLink);
    }
  }

  window.addEventListener("scroll", scheduleActiveLink, { passive: true });
  window.addEventListener("resize", scheduleActiveLink);
  window.addEventListener("hashchange", scheduleActiveLink);
  setActiveLink();

  const mobileQuery = window.matchMedia("(max-width: 56rem)");
  const details = toc.querySelector("details");

  function keepDesktopTocOpen(event) {
    if (!event.matches && details) details.open = true;
  }

  if (mobileQuery.addEventListener) {
    mobileQuery.addEventListener("change", keepDesktopTocOpen);
  }

  tocNav.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    if (details && mobileQuery.matches) {
      details.open = false;
    }
  });
})();
