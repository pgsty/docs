import type { ReactNode } from 'react';
import { HomeLayout } from 'fumadocs-ui/layouts/home';
import { baseOptions, linkItems } from '@/app/layout.config';

export default async function Layout({
  children,
  params
}: {
  children: ReactNode;
  params: Promise<{ lang: string }>
}) {
  const lang = (await params).lang;

  return (
    <HomeLayout
      {...baseOptions(lang)}
      links={linkItems(lang)}
      className="dark:bg-neutral-950 dark:[--color-fd-background:var(--color-neutral-950)] pt-0"
      nav={{
        enabled: false,
      }}
    >
      {children}
    </HomeLayout>
  );
}
