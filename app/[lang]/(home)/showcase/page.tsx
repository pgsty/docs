import { PlusIcon } from 'lucide-react';
import Image, { type StaticImageData } from 'next/image';
import { cn } from '@/lib/cn';
import { buttonVariants } from '@/components/ui/button';
import Link from 'next/link';


interface ShowcaseObject {
  image?: StaticImageData;
  name: string;
  url: string;
}

const showcases: ShowcaseObject[] = [
  {
    name: 'Dirstarter',
    url: 'https://dirstarter.com',
  },
  {
    name: 'Rehooks',
    url: 'https://rehooks.pyr33x.ir',
  },
  {
    name: 'Typelytics',
    url: 'https://typelytics.rhyssul.com',
  },
  {
    name: 'Swellchain',
    url: 'https://build.swellnetwork.io',
  },
  {
    name: 'ESLint React',
    url: 'https://eslint-react.xyz',
  },
  {
    name: 'nextjs i18n docs',
    url: 'https://nextjs.im',
  },
];

const blogs: ShowcaseObject[] = [
  {
    name: "RUNFUNRUN's Blog",
    url: 'https://runfunrun.dev',
  },
  {
    name: 'xlog.systems',
    url: 'https://www.xlog.systems',
  },
  {
    name: 'stutuer',
    url: 'https://www.stutuer.tech',
  },
];

const vercel = [
  {
    name: 'Turbo',
    url: 'https://turbo.build',
  },
  {
    name: 'Flags SDK',
    url: 'https://flags-sdk.dev',
  },
  {
    name: 'Chat SDK',
    url: 'https://chat-sdk.dev',
  },
];

export default function Showcase() {
  return (
    <main className="px-4 py-12 z-[2] w-full max-w-[1400px] mx-auto [--color-fd-border:color-mix(in_oklab,var(--color-fd-primary)_30%,transparent)]">
      <div className="relative overflow-hidden border border-dashed p-6">
        <h1 className="mb-4 text-xl font-medium">
          The docs framework designed with care.
        </h1>
        <p className="text-fd-muted-foreground">
          A list of beautiful open-source projects with their docs powered by
          Fumadocs.
        </p>
        <div className="mt-6">
          <a
            href="https://github.com/fuma-nama/fumadocs/discussions/30"
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
        <span className="absolute text-xs left-6 bottom-6 text-fd-muted-foreground font-mono">
          Showcases
        </span>

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
            Fumadocs powers the docs of Vercel open source SDKs.
          </h2>
          <div className="flex items-center gap-2 -mx-1.5">
            {vercel.map((item) => (
              <Link
                key={item.url}
                href={item.url}
                className={cn(
                  buttonVariants({
                    variant: 'link',
                    size: 'xs',
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
            href="https://github.com/fuma-nama/fumadocs/discussions/30"
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
        Fumadocs can power your blog, too.
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
