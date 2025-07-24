import "@/app/global.css"
import { RootProvider } from 'fumadocs-ui/provider';
import type { Translations } from 'fumadocs-ui/i18n';
import { Analytics } from '@vercel/analytics/react';
import type { Metadata } from 'next';

const zh: Partial<Translations> = {
  search: '搜索',
  searchNoResult: '未找到',
  toc: '目录',
  tocNoHeadings: '目录',
  lastUpdate: '最后更新',
  chooseLanguage: '选择语言',
  nextPage: '下一页',
  previousPage: '上一页',
  chooseTheme: '选择主题',
  editOnGithub: '编辑',
};

const locales = [
  {name: 'English', locale: 'en'},
  {name: '简体中文', locale: 'zh'},
];

// SEO metadata configuration
const siteConfig = {
  en: {
    title: 'Pigsty, FOSS Postgres RDS',
    description: 'Pigsty is a Battery-Included, Local-First PostgreSQL Distribution as a Free & Better RDS Alternative!',
    keywords: 'pigsty, pgsty, pig, postgresql, postgres, rds, extensions, supabase, ansible, grafana, patroni, pgbackrest, observability',
    siteName: 'Pigsty',
  },
  zh: {
    title: 'Pigsty, 开源 PG RDS',
    description: 'Pigsty是一个开箱即用的 PostgreSQL 发行版，本地优先的开源云数据库！',
    keywords: 'pigsty, pgsty, pig, postgresql, postgres, RDS, PG扩展, 数据库, 文档, PG高可用, PG监控, supabase, ansible, grafana, patroni, pgbackrest, observability',
    siteName: 'Pigsty',
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string }>;
}): Promise<Metadata> {
  const lang = (await params).lang as 'en' | 'zh';
  const config = siteConfig[lang] || siteConfig.en;

  return {
    title: {
      default: config.title,
      template: `%s | ${config.siteName}`,
    },
    description: config.description,
    keywords: config.keywords,
    authors: [{ name: 'Vonng' }],
    creator: 'Vonng',
    publisher: 'Pigsty',
    metadataBase: new URL('https://doc.pgsty.com'),
    alternates: {
      canonical: '/',
      languages: {
        'en': '/',
        'zh': '/zh',
      },
    },
    openGraph: {
      type: 'website',
      locale: lang === 'zh' ? 'zh_CN' : 'en_US',
      url: '/',
      siteName: config.siteName,
      title: config.title,
      description: config.description,
      images: [
        {
          url: '/img/pigsty/og.jpg',
          width: 1200,
          height: 630,
          alt: config.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: config.title,
      description: config.description,
      images: ['/img/pigsty/og.jpg'],
      creator: '@Vonng',
    },
    robots: {
      index: true,
      follow: true,
      googleBot: {
        index: true,
        follow: true,
        'max-video-preview': -1,
        'max-image-preview': 'large',
        'max-snippet': -1,
      },
    },
    verification: {
      google: 'your-google-verification-code',
      yandex: 'your-yandex-verification-code',
    },
    category: 'technology',
  };
}

export default async function RootLayout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  return (
    <html lang={lang} suppressHydrationWarning>
      <body>
        <RootProvider
          i18n={{
            locale: lang,
            locales,
            translations: { zh }[lang],
          }}
        >
          {children}
        </RootProvider>
        <Analytics />
      </body>
    </html>
  );
}