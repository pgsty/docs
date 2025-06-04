import { PlusIcon } from 'lucide-react';
import Image, { type StaticImageData } from 'next/image';
import { cn } from '@/lib/cn';
import { buttonVariants } from '@/components/ui/button';
import Link from 'next/link';

import UserAirwallex      from '@/public/img/user/airwallex.png';
import UserBilibili       from '@/public/img/user/bilibili.png';
import UserBitdeer        from '@/public/img/user/bitdeer.png';
import UserHuafon         from '@/public/img/user/huafon.png';
import UserLinkfog        from '@/public/img/user/linkfog.png';
import UserMeitu          from '@/public/img/user/meitu.png';
import UserMomenta        from '@/public/img/user/momenta.png';
import UserMotphys        from '@/public/img/user/motphys.png';
import UserOCI            from '@/public/img/user/oci.png';
import UserPolardb        from '@/public/img/user/polardb.png';
import UserTantan         from '@/public/img/user/tantan.png';
import UserYSJF           from '@/public/img/user/ysjf.png';

interface ShowcaseObject {
  image?: StaticImageData;
  name: string;
  url: string;
}

const showcases: ShowcaseObject[] = [
  {
    name: 'MediaStorm',
    image: UserYSJF,
    url: 'https://www.ysjf.com/',
  },
  {
    name: 'HuaFon',
    image: UserHuafon,
    url: 'https://www.huafeng.com/en/',
  },
  {
    name: 'BitDeer',
    image: UserBitdeer,
    url: 'https://www.bitdeer.com/',
  },
  {
    name: 'LinkFog',
    image: UserLinkfog,
    url: 'https://www.linkfog.com/',
  },
  {
    name: 'Momenta',
    image: UserMomenta,
    url: 'https://www.momenta.cn/',
  },
  {
    name: 'Motphys',
    image: UserMotphys,
    url: 'https://www.motphys.com/',
  },
  {
    name: 'Oracle Cloud',
    image: UserOCI,
    url: 'https://www.oracle.com/cloud/',
  },
  {
    name: 'Aliyun PolarDB',
    image: UserPolardb,
    url: 'https://www.alibabacloud.com/help/en/polardb/product-overview/',
  },
  {
    name: 'BiliBili',
    image: UserBilibili,
    url: 'http://www.bilibili.com/',
  },
  {
    name: 'AirWallex',
    image: UserAirwallex,
    url: 'https://www.airwallex.com/us/',
  },
  {
    name: 'TanTan App',
    image: UserTantan,
    url: 'https://tantanapp.com/',
  },
  {
    name: 'Meitu',
    image: UserMeitu,
    url: 'https://meitu.com/',
  },
];

const blogs: ShowcaseObject[] = [
  {
    name: 'Supabase',
    url: 'https://pigsty.io/docs/app/supabase',
  },
  {
    name: 'Odoo',
    url: 'https://pigsty.io/docs/app/odoo',
  },
  {
    name: 'Dify',
    url: 'https://pigsty.io/docs/app/dify',
  },
];

const vercel = [
  {
    name: 'Supabase',
    url: 'https://pigsty.io/docs/app/supabase',
  },
  {
    name: 'Odoo',
    url: 'https://pigsty.io/docs/app/odoo',
  },
  {
    name: 'Dify',
    url: 'https://pigsty.io/docs/app/dify',
  },
];

export default function Showcase() {
  return (
    <main className="px-4 py-12 z-[2] w-full max-w-[1400px] mx-auto [--color-fd-border:color-mix(in_oklab,var(--color-fd-primary)_30%,transparent)]">
      <div className="relative overflow-hidden border border-dashed p-6">
        <h1 className="mb-4 text-xl font-medium">
          The self-hosting dbms infra designed with love & care.
        </h1>
        <p className="text-fd-muted-foreground">
          A list of users & customers with their projects powered by Pigsty
        </p>
        <div className="mt-6">
          <a
            href="https://github.com/orgs/pgsty/discussions/600"
            target="_blank"
            rel="noreferrer noopener"
            className={cn(
              buttonVariants({
                variant: 'outline',
              }),
            )}
          >
            <PlusIcon className="me-2 size-4" />
            Suggest Yours
          </a>
        </div>


      </div>

      <div className="flex gap-4 border border-dashed p-6 mt-6">
        <svg
          aria-label="Vercel logomark"
          height="64"
          role="img"
          viewBox="0 0 74 64"
          className="size-6 mt-1"
        >
          <path
            d="M37.5896 0.25L74.5396 64.25H0.639648L37.5896 0.25Z"
            fill="currentColor"
          />
        </svg>
        <div>
          <h2 className="text-sm font-medium mb-2">
            Pigsty has the following modules available in addition to PostgreSQL database.
          </h2>
          <div className="flex items-center gap-2 -mx-1.5">
            {vercel.map((item) => (
              <Link
                key={item.url}
                href={item.url}
                className={cn(
                  buttonVariants({
                    variant: 'link',
                    size: 'sm',
                  }),
                  'text-fd-muted-foreground',
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
      <div className="relative mt-6 grid gap-2.5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {showcases.map((showcase) => (
          <ShowcaseItem key={showcase.url} {...showcase} />
        ))}
        <div className="absolute text-center bottom-0 inset-x-0 pt-4 bg-gradient-to-t from-fd-background">
          <Link
            href="https://github.com/orgs/pgsty/discussions/600"
            className={cn(
              buttonVariants({
                size: 'sm',
                variant: 'link',
              }),
            )}
          >
            See all of our showcases.
          </Link>
        </div>
      </div>
      <h2 className="text-xl font-medium mt-12 px-4">
        Pigsty can serve enterprise software, too
      </h2>
      <div className="mt-6 grid gap-2.5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {blogs.map((showcase) => (
          <ShowcaseItem key={showcase.url} {...showcase} />
        ))}
      </div>
    </main>
  );
}

function ShowcaseItem({ name, url, image }: ShowcaseObject) {
  if (image) {
    return (
      <a
        href={url}
        target="_blank"
        rel="noreferrer noopener"
        className="group relative aspect-[1.91/1] border border-dashed"
      >
        <Image
          alt="Preview"
          src={image}
          placeholder="blur"
          fill
          sizes="100vw, (min-width: 750px) 500px"
          className="transition-all group-hover:brightness-150"
        />
        <p className="absolute bottom-0 inset-x-0 z-[2] bg-fd-background px-4 py-2 text-sm font-medium">
          {name}
        </p>
      </a>
    );
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noreferrer noopener"
      className="flex aspect-[1.91/1] flex-col border border-dashed p-4 transition-all hover:bg-fd-accent"
    >
      <p className="font-mono text-xs mb-2 text-fd-muted-foreground">
        {new URL(url).hostname}
      </p>
      <p className="text-xl font-medium">{name}</p>
    </a>
  );
}
