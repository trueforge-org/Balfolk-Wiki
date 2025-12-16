import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
// TODO: reenable
// https://github.com/HiDeoo/starlight-links-validator
//import starlightLinksValidator from "starlight-links-validator";
// https://github.com/HiDeoo/starlight-image-zoom
import starlightImageZoom from "starlight-image-zoom";
// https://docs.astro.build/en/guides/integrations-guide/sitemap/
import sitemap from "@astrojs/sitemap";
// https://github.com/alextim/astro-lib/tree/main/packages/astro-robots-txt#readme
import robotsTxt from "astro-robots-txt";
// https://github.com/giuseppelt/astro-lottie
import lottie from "astro-integration-lottie";
// https://github.com/risu729/astro-better-image-service
import betterImageService from "astro-better-image-service";
// https://github.com/Playform/Compress
import playformCompress from "@playform/compress";
const site = "https://balfolk-wiki.trueforge.org";

// https://astro.build/config
export default defineConfig({
  site: site,
  base: "/",
  output: "static",
  outDir: "build",
  cacheDir: ".astro/cache",
  trailingSlash: "ignore",
  compressHTML: true,
  prefetch: {
    prefetchAll: true,
  },
  build: {
    output: "directory",
  },
  experimental: {
  },
  integrations: [
    starlight({
      title: "Balfolk-Wiki",
      customCss: ["./src/tailwind.css"],
      tagline: "Balfolk-Wiki - The community driven Balfolk dance wiki",
      pagefind: true,
      logo: {
        src: "./src/assets/with-text.svg",
        replacesTitle: true,
      },
      head: [
        {
          tag: "script",
          attrs: {
            src: "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9270569596814796",
            crossorigin: "anonymous",
            defer: true,
          },
        },
        {
          tag: "script",
          attrs: {
            src: "https://www.googletagmanager.com/gtag/js?id=G-Q9NT692BZZ",
            defer: true,
          },
        },
        {
          tag: "script",
          content:
            "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-Q9NT692BZZ');",
        },
      ],
      tableOfContents: {
        maxHeadingLevel: 6,
      },
      social: [
      ],
      editLink: {
        baseUrl: "https://github.com/trueforge-org/balfolk-wiki/tree/main",
      },
      components: {
        Header: "./src/components/CustomHeader.astro",
        Sidebar: "./src/components/CustomSidebar.astro",
        // Hero: "./src/components/CustomHero.astro",
        // MarkdownContent: "./src/components/CustomMarkdownContent.astro",
      },
      plugins: [
        // starlightBlog({
        //   prefix: "news",
        //   title: "TrueCharts News",
        //   postCount: 5,
        //   recentPostCount: 10,
        //   authors: authors,
        // }),
        starlightImageZoom(),
        //starlightLinksValidator({
        //  errorOnRelativeLinks: false,
        //  errorOnFallbackPages: false,
        //  errorOnLocalLinks: false,
        //  exclude: [
        //    "/s/charts",
        //    "/s/discord",
        //    "/s/fb",
        //    "/s/ghs",
        //    "/s/git",
        //    "/s/oc",
        //    "/s/patreon",
        //    "/s/shop",
        //    "/s/tg",
        //    "/s/twitter",
        //  ],
        //}),
      ],
      sidebar: [
        {
          label: "algemeen",
          collapsed: true,
          autogenerate: {
            directory: "algemeen",
          },
        },
        {
          label: "dansen",
          collapsed: true,
          autogenerate: {
            directory: "dansen",
          },
        },
        {
          label: "overige",
          collapsed: true,
          autogenerate: {
            directory: "overige",
          },
        },
      ],
    }),
    sitemap(),
    robotsTxt(),
    lottie(),
    betterImageService(),
    playformCompress({
      HTML: false,
      CSS: true,
      JavaScript: true,
      Image: true,
      SVG: true,
    }),
  ],
});
