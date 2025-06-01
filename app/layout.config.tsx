import type { BaseLayoutProps, LinkItemType } from 'fumadocs-ui/layouts/shared';
import { i18n } from '@/lib/i18n';
import { AlbumIcon } from 'lucide-react';
import { LayoutTemplate } from 'lucide-react';

export const linkItems: LinkItemType[] = [
  {
    icon: <AlbumIcon />,
    text: 'Blog',
    url: '/blog',
    active: 'nested-url',
  },
  {
    text: 'Showcase',
    url: '/showcase',
    icon: <LayoutTemplate />,
    active: 'url',
  },
];

export const baseOptions = (lang: string): BaseLayoutProps => {
  return {
    i18n,
    nav: {
      title: (
        <>
          <svg
            width="24"
            height="24"
            xmlns="http://www.w3.org/2000/svg"
            aria-label="Logo"
          >
            <circle cx={12} cy={12} r={12} fill="currentColor" />
          </svg>
          Pigsty
        </>
      ),
    },
    // see https://fumadocs.dev/docs/ui/navigation/links
    links: [],
  }
}