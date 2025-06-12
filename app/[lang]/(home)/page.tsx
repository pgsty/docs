import { cva } from 'class-variance-authority';
import {
    BatteryChargingIcon,
    type LucideIcon,
    MousePointer,
    FileCode,
    TimerIcon,
    SquareCode, Telescope, Zap, DatabaseBackup, Cpu, Infinity, BookDashed, Cuboid,
} from 'lucide-react';
import { File, Files, Folder } from 'fumadocs-ui/components/files';
import Link from 'next/link';
import type { ReactNode } from 'react';
import Image from 'next/image';
import { cn } from '@/lib/cn';
import { buttonVariants } from '@/components/ui/button';
import { CodeBlock } from '@/components/code-block';
import { UwuHero } from '@/app/[lang]/(home)/uwu';
import {
    CreateAppAnimation,
    PreviewImages,
    WhyInteractive,
} from './page.client';

import HaImg from '@/public/img/pigsty/ha.png';
import EcosystemImg from '@/public/img/pigsty/ecosystem.gif';
import DistroImg from '@/public/img/pigsty/distro.gif';

const badgeVariants = cva(
    'inline-flex size-7 items-center justify-center rounded-full bg-fd-primary font-medium text-fd-primary-foreground',
);

export default function Page() {
    const gridColor =
        'color-mix(in oklab, var(--color-fd-primary) 10%, transparent)';

    return (
        <>
            <div
                className="absolute inset-x-0 top-[360px] h-[250px] max-md:hidden"
                style={{
                    background: `repeating-linear-gradient(to right, ${gridColor}, ${gridColor} 1px,transparent 1px,transparent 50px), repeating-linear-gradient(to bottom, ${gridColor}, ${gridColor} 1px,transparent 1px,transparent 50px)`,
                }}
            />
            <main className="container relative max-w-[1100px] px-2 py-4 z-[2] lg:py-8">
                <div
                    style={{
                        background:
                            'repeating-linear-gradient(to bottom, transparent, color-mix(in oklab, var(--color-fd-primary) 1%, transparent) 500px, transparent 1000px)',
                    }}
                >
                    <div className="relative">
                        <Hero />
                        <UwuHero />
                    </div>
                    <Introduction />
                    <Alternative />
                    <Distribution />
                    <Highlights />
                    <Why />
                    <End />
                </div>
            </main>
        </>
    );
}

function Alternative() {
    return (
        <div className="flex flex-col gap-8 border-x border-t p-8 md:px-12 lg:flex-row lg:items-center">
            <div className="text-start lg:flex-1">
                <Link href="/docs/intro/rds">
                <p className="px-2 py-1 text-sm font-mono bg-fd-primary text-fd-primary-foreground font-bold w-fit mb-4">
                    The FOSS RDS Alternative
                </p>
                </Link>
                <Link href="/docs/intro/rds">
                <h2 className="text-2xl font-semibold mb-4">A Gift to the Community</h2>
                </Link>
                <h5 className="text-sm  mb-3">DBA as a Software, written for ourselves. Self-hosting PG Like a Pro!</h5>
                <p className="text-fd-muted-foreground mb-6">
                    Pigsty turn the kernels and OSS tools into a integrated solution,
                    makes it easy to self-hosting your own production-grade RDS.
                    Launch without DBA expertise, save 90%+ cost than cloud RDS.
                </p>
            </div>
            <div className="lg:flex-1 flex justify-center items-center">
                <Link href="/docs/intro/rds"><Image
                    src={DistroImg}
                    alt="RDS Alternative"
                    className="w-full h-auto max-w-none"
                /></Link>
            </div>
        </div>
    );
}

function Distribution() {
    return (
        <div className="flex flex-col gap-4 border-x border-t p-8 md:px-12">
            <div className="text-start">
                <Link href="/docs/intro/distro">
                <p className="px-2 py-1 text-sm font-mono bg-fd-primary text-fd-primary-foreground font-bold w-fit mb-4">
                    The PG Database Distribution
                </p>
                </Link>
                <Link href="/docs/intro/distro">
                <h2 className="text-2xl font-semibold mb-4">Unite the PG Ecosystem</h2>
                </Link>
                <h5 className="text-sm  mb-3">PostgreSQL is eating the database world, Let&apos;s unite these extension superpowers!</h5>
                <p className="text-fd-muted-foreground mb-6">
                    Harness the superpower of PostgreSQL ecosystem! with unparalleled 420+ extensions.
                    Simulate Oracle, MySQL, MSSQL, MONGO with exotic kernels, self-hosting Supabase, scaling with citus; analytic with duckdb;
                    Explore the world of possibility and maximize the synergistic effect of the ecosystem. Just use PostgreSQL for Everything, and it&apos;s time to conquer the database world with postgres.
                </p>
            </div>
            <Image
                src={EcosystemImg}
                alt="Ecosystem"
                className="w-full max-w-full h-auto mt-2 dark:invert"
            />
        </div>
    );
}

async function Why() {
    return (
        <div className="relative overflow-hidden border-x border-t p-2">
            <WhyInteractive></WhyInteractive>
        </div>
    );
}

function End() {
    return (
        <div className="flex flex-col border-b border-r md:flex-row *:border-l *:border-t">
            <div className="group flex flex-col min-w-0 flex-1 pt-8 **:transition-colors">
                <h2 className="text-3xl text-center font-extrabold font-mono uppercase text-fd-muted-foreground mb-4 lg:text-4xl group-hover:text-blue-500">
                    Self-Hosting like a Pro
                </h2>
                <p className="text-center font-mono text-xs text-fd-foreground/60 mb-8 group-hover:text-blue-500/80">
                    Everything you need for a production-grade PostgreSQL service
                </p>
                <div className="h-[200px] overflow-hidden p-8 bg-gradient-to-b from-fd-primary/10 group-hover:from-blue-500/10">
                    <div className="mx-auto bg-radial-[circle_at_0%_100%] from-60% from-transparent to-fd-primary size-[500px] rounded-full group-hover:from-blue-500 group-hover:to-blue-600/10" />
                </div>
            </div>
            <ul className="flex flex-col gap-4 p-6 pt-8">
                <li>
                    <span className="flex flex-row items-center gap-2 font-medium">
                        <BatteryChargingIcon className="size-5" />
                        Battery Included
                    </span>
                    <span className="mt-2 text-sm text-fd-muted-foreground">
                        All you need for enterprise PostgreSQL, out of the box
                    </span>
                </li>
                <li>
                    <span className="flex flex-row items-center gap-2 font-medium">
                        <svg viewBox="0 0 24 24" className="size-5" fill="currentColor">
                            <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
                        </svg>
                        Open Source
                    </span>
                    <span className="mt-2 text-sm text-fd-muted-foreground">
                        100% open-source, FOSS license, community-driven
                    </span>
                </li>
                <li>
                    <span className="flex flex-row items-center gap-2 font-medium">
                        <TimerIcon className="size-5" />
                        Local-First
                    </span>
                    <span className="mt-2 text-sm text-fd-muted-foreground">
                        Run anywhere, own your data, no more vendor lock-in
                    </span>
                </li>
                <li className="flex flex-row flex-wrap gap-2 mt-auto">
                    <Link href="/docs/install" className={cn(buttonVariants())}>
                        Get Started
                    </Link>
                    <a
                        href="http://demo.pigsty.cc"
                        rel="noreferrer noopener"
                        className={cn(
                            buttonVariants({
                                variant: 'outline',
                            }),
                        )}
                    >
                        Open Demo
                    </a>
                </li>
            </ul>
        </div>
    );
}

function Highlights(): React.ReactElement {
    return (
        <div className="grid grid-cols-1 border-r md:grid-cols-2 lg:grid-cols-3">
            <div className="col-span-full flex flex-row items-start justify-center border-l border-t p-8 pb-2 text-center">
                <h2 className="bg-fd-primary text-fd-primary-foreground px-1 text-2xl font-semibold">
                    Highlights
                </h2>
                <MousePointer className="-ml-1 mt-8" />
            </div>
            <Link href="/docs/feat/ext"><Highlight icon={TimerIcon} heading="Extension Overwhelming">
                Gather the superpower of 420+ PG Extensions out-of-the-box together
            </Highlight></Link>

            <Link href="/docs/feat/ha"><Highlight icon={Infinity} heading="High-Availability">
                Self-Healing architecture with reliable services access, 0-downtime migration
            </Highlight></Link>

            <Link href="/docs/feat/infra"><Highlight icon={Telescope} heading="Observability Stack">
                Prometheus & Grafana best practice. Dashboards with unparalleled visibility
            </Highlight></Link>

            <Link href="/docs/feat/kernel"><Highlight icon={Cpu} heading="PG Kernel Replacement">
                Simulating Oracle, MySQL, SQL Server, and MongoDB with exotic kernel forks
            </Highlight></Link>

            <Link href="/docs/feat/pitr"><Highlight icon={DatabaseBackup} heading="Enterprise Security">
                Auto configured PITR, Backup Encryption, ACL Model, Local CA, SSL Certs, AuditLog
            </Highlight></Link>

            <Link href="/docs/feat/iac"><Highlight icon={SquareCode} heading="Infrastructure as Code">
                Describe and materialize entire infra & database clusters with code & playbook
            </Highlight></Link>

            <Link href="/docs/app/supabase"><Highlight icon={Zap} heading="Self-Hosting Supabase">
                Tun postgres into a full-featured BaaS, Migration in an hour, scale to billion
            </Highlight></Link>

            <Link href="/docs/feat/raw"><Highlight icon={Cuboid} heading="No Container / Raw Linux">
                Run directly on mainstream Linux distros. No need for containers & kubernetes
            </Highlight></Link>

            <Link href="/docs/app"><Highlight icon={BookDashed} heading="Application Templates">
                Launch enterprise software like Odoo, Dify, Gitlab, Jira, Wiki.js, Gitea at ease
            </Highlight></Link>

</div>
    );
}

function Highlight({
                       icon: Icon,
                       heading,
                       children,
                   }: {
    icon: LucideIcon;
    heading: ReactNode;
    children: ReactNode;
}): React.ReactElement {
    return (
        <div className="border-l border-t px-6 py-12">
            <div className="mb-4 flex flex-row items-center gap-2 text-fd-muted-foreground">
                <Icon className="size-4" />
                <h2 className="text-sm font-medium">{heading}</h2>
            </div>
            <span className="font-medium">{children}</span>
        </div>
    );
}

function Hero() {
    return (
        <div className="relative z-[2] flex flex-col border-x border-t bg-fd-background/80 px-4 pt-12 max-md:text-center md:px-12 md:pt-16 [.uwu_&]:hidden overflow-hidden">
            <div
                className="absolute inset-0 z-[-1] blur-2xl hidden dark:block"
                style={{
                    maskImage:
                        'linear-gradient(to bottom, transparent, white, transparent)',
                    background:
                        'repeating-linear-gradient(65deg, var(--color-blue-500), var(--color-blue-500) 12px, color-mix(in oklab, var(--color-blue-600) 30%, transparent) 20px, transparent 200px)',
                }}
            />
            <div
                className="absolute inset-0 z-[-1] blur-2xl dark:hidden"
                style={{
                    maskImage:
                        'linear-gradient(to bottom, transparent, white, transparent)',
                    background:
                        'repeating-linear-gradient(65deg, var(--color-purple-300), var(--color-purple-300) 12px, color-mix(in oklab, var(--color-blue-600) 30%, transparent) 20px, transparent 200px)',
                }}
            />
            <h1 className="mb-8 text-4xl font-medium md:hidden">Build Your Docs</h1>
            <h1 className="mb-8 max-w-[600px] text-4xl font-medium max-md:hidden">
                PostgreSQL in Great STYle
            </h1>
            <p className="mb-8 text-fd-muted-foreground md:max-w-[80%] md:text-xl">
                Battery-Included, Open-Source, Local-First PostgreSQL Distribution
            </p>
            <div className="inline-flex items-center gap-3 max-md:mx-auto">
                <Link
                    href="/docs/"
                    className={cn(
                        buttonVariants({ size: 'lg', className: 'rounded-full' }),
                    )}
                >
                    Get Started
                </Link>
                <a
                    href="http://demo.pigsty.cc"
                    target="_blank"
                    rel="noreferrer noopener"
                    className={cn(
                        buttonVariants({
                            size: 'lg',
                            variant: 'outline',
                            className: 'rounded-full bg-fd-background',
                        }),
                    )}
                >
                    Live Demo
                </a>
            </div>
            <PreviewImages />
        </div>
    );
}

const feedback = [
    {
        avatar: 'https://avatars.githubusercontent.com/u/124599',
        user: 'shadcn',
        role: 'Creator of Shadcn UI',
        message: `You know how you end up rebuilding a full docs site every time you start a new project? 

Fumadocs fixes this by giving you all the right blocks that you compose together.

Like headless docs to build exactly what you need.`,
    },
    {
        avatar: 'https://avatars.githubusercontent.com/u/35677084',
        user: 'Anthony Shew',
        role: 'Turbo DX at Vercel',
        message: `Major shoutout to @fuma_nama for making fumadocs, a gorgeous documentation framework that composes beautifully into the App Router.`,
    },
    {
        user: 'Aiden Bai',
        avatar: 'https://avatars.githubusercontent.com/u/38025074',
        role: 'Creator of Million.js',
        message: 'fumadocs is the best Next.js docs framework',
    },
    {
        avatar: 'https://avatars.githubusercontent.com/u/10645823',
        user: 'David Blass',
        role: 'Creator of Arktype',
        message: `I'd have no shot building @arktypeio docs that looked half this good without it 😍`,
    },    {
        avatar: 'https://avatars.githubusercontent.com/u/35677084',
        user: 'aAnthony Shew',
        role: 'Turbo DX at Vercel',
        message: `Major shoutout to @fuma_nama for making fumadocs, a gorgeous documentation framework that composes beautifully into the App Router.`,
    },
    {
        user: 'aAiden Bai',
        avatar: 'https://avatars.githubusercontent.com/u/38025074',
        role: 'Creator of Million.js',
        message: 'fumadocs is the best Next.js docs framework',
    },
    {
        avatar: 'https://avatars.githubusercontent.com/u/10645823',
        user: 'aDavid Blass',
        role: 'Creator of Arktype',
        message: `I'd have no shot building @arktypeio docs that looked half this good without it 😍`,
    }
];

function Introduction(): React.ReactElement {
    return (
        <div className="grid grid-cols-1 border-r md:grid-cols-2">

            <div className="flex flex-col gap-2 border-l border-t px-6 py-12 md:py-16">
                <Link href="/docs/install/start"><div className={cn(badgeVariants())}>1</div></Link>
                <Link href="/docs/install/start"><h3 className="text-xl font-semibold">Install Pigsty</h3></Link>
                <p className="mb-8 text-fd-muted-foreground">
                    One command to <Link className="font-bold text-sky-500" href="/docs/install/start">install</Link> PostgreSQL RDS with  <Link className="font-bold text-sky-500" href="https://ext.pigsty.io">420+</Link> extensions.
                </p>
                <CreateAppAnimation />
            </div>

            <div className="flex flex-col gap-2 border-l border-t px-6 py-12 md:py-16">

                <Link href="/docs/install/multinode"><div className={cn(badgeVariants())}>2</div></Link>
                <Link href="/docs/install/multinode"><h3 className="text-xl font-semibold">Deploy Clusters</h3></Link>

                <p className="text-fd-muted-foreground">
                    Spin up  <Link className="font-bold text-sky-500" href="/docs/install/multinode">multi-node</Link>, self-healing HA Database Clusters with code.
                </p>
                <div className="relative flex flex-col">
                    <CodeBlock
                        lang="yaml"
                        wrapper={{
                            className: 'absolute inset-x-2 top-0 shadow-lg',
                        }}
                        code={`pg-prod:
  hosts:
    10.10.10.11: { pg_seq: 1, pg_role: primary }
    10.10.10.12: { pg_seq: 2, pg_role: replica }
    10.10.10.13: { pg_seq: 3, pg_role: offline }
  vars: { pg_cluster: pg-prod }
`}
                    />
                    <Files className="z-[2] mt-40 shadow-xl">
                        <Folder name="pigsty" defaultOpen>
                            <a href={"/docs/config/inventory"}><File name="pigsty.yml" icon={<FileCode className="text-blue-500" />} /></a>
                            <a href={"/docs/pgsql/playbook"}><File name="pgsql.yml" icon={<Cpu className="text-orange-500" />} /></a>
                        </Folder>
                    </Files>
                </div>
            </div>

            <div className="col-span-full flex flex-col items-center gap-2 border-l border-t px-6 py-16 text-center">
                <div className={cn(badgeVariants())}>3</div>
                <h3 className="text-2xl font-semibold">Deliver Service</h3>
                <p className="text-fd-muted-foreground">
                    <span>Deliver enterprise-grade database service in minutes, </span> without caring about details.
                </p><br /><br />
                <div className="mt-4 flex flex-row flex-wrap items-center gap-8">
                    <Image
                        src={HaImg}
                        alt="Architecture"
                        className="mx-auto -my-16 w-full max-w-[1200px] lg:max-w-[1400px] xl:max-w-[1600px] lg:mx-0"
                    />
                </div>
                <br />
            </div>
        </div>
    );
}

