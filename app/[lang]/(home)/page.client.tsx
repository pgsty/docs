'use client';

import {
  Fragment,
  type HTMLAttributes,
  type HTMLProps,
  type ReactElement,
  type ReactNode,
  useEffect,
  useState,
} from 'react';
import { TerminalIcon } from 'lucide-react';

import scrollIntoView from 'scroll-into-view-if-needed';
import { cn } from '@/lib/cn';
import Image from 'next/image';
import { Cards, Card } from 'fumadocs-ui/components/card';
import DistributionImg from '@/public/img/pigsty/distribution.png';
import DashboardImg from '@/public/img/pigsty/dashboard.gif';
import ExtensionImg from '@/public/img/pigsty/extension.png';

import { cva } from 'class-variance-authority';

export function CreateAppAnimation() {
  const installCmd = 'curl https://repo.pigsty.io/get | bash -s v3.5.0';
  const tickTime = 30;
  const timeCommandEnter = installCmd.length;
  const timeCommandRun = timeCommandEnter + 3;
  const timeCommandEnd = timeCommandRun + 3;
  const timeWindowOpen = timeCommandEnd + 1;
  const timeEnd = timeWindowOpen + 1;

  const [tick, setTick] = useState(timeEnd);

  useEffect(() => {
    const timer = setInterval(() => {
      setTick((prev) => (prev >= timeEnd ? prev : prev + 1));
    }, tickTime);

    return () => {
      clearInterval(timer);
    };
  }, [timeEnd]);

  const lines: ReactElement[] = [];

  lines.push(
    <span key="command_type">
      {installCmd.substring(0, tick)}
      {tick < timeCommandEnter && (
        <div className="inline-block h-3 w-1 animate-pulse bg-white" />
      )}
    </span>,
  );

  if (tick >= timeCommandEnter) {
    lines.push(<span key="space"> </span>);
  }

  if (tick > timeCommandRun)
    lines.push(
      <Fragment key="command_response">
        {tick > timeCommandRun + 1 && (
          <>
            <span className="font-bold">$ cd ~/pigsty</span>
          </>
        )}
        {tick > timeCommandRun + 2 && (
          <>
            <span className="font-bold">$ ./bootstrap</span>
          </>
        )}
        {tick > timeCommandRun + 3 && (
          <>
            <span className="font-bold">$ ./configure</span>
          </>
        )}
        {tick > timeCommandRun + 4 && (
            <>
              <span className="font-bold">$ ./install.yml</span>
            </>
        )}
      </Fragment>,
    );

  return (
    <div
      className="relative"
      onMouseEnter={() => {
        if (tick >= timeEnd) {
          setTick(0);
        }
      }}
    >
      {tick > timeWindowOpen && (
        <LaunchAppWindow className="absolute bottom-5 right-4 z-10 animate-in fade-in slide-in-from-top-10" />
      )}
      <pre className="overflow-hidden rounded-xl border text-[13px] shadow-lg">
        <div className="flex flex-row items-center gap-2 border-b px-4 py-2">
          <TerminalIcon className="size-4" />{' '}
          <span className="font-bold">Terminal</span>
          <div className="grow" />
          <div className="size-2 rounded-full bg-red-400" />
        </div>
        <div className="min-h-[200px] bg-gradient-to-b from-fd-card">
          <code className="grid p-4">{lines}</code>
        </div>
      </pre>
    </div>
  );
}

function LaunchAppWindow(
  props: HTMLAttributes<HTMLDivElement>,
): React.ReactElement {
  return (
    <div
      {...props}
      className={cn(
        'overflow-hidden rounded-md border bg-fd-background shadow-xl',
        props.className,
      )}
    >
      <div className="relative flex h-6 flex-row items-center border-b bg-fd-muted px-4 text-xs text-fd-muted-foreground">
        <p className="absolute inset-x-0 text-center">localhost:3000</p>
      </div>
      <div className="p-4 text-sm">New App launched!</div>
    </div>
  );
}

export function WhyInteractive(props: {
  codeblockTheme: ReactNode;
  codeblockSearchRouter: ReactNode;
  codeblockInteractive: ReactNode;
  typeTable: ReactNode;
  codeblockMdx: ReactNode;
}) {
  const [active, setActive] = useState(0);
  const items = [
    'Extensible Postgres',
    'Reliable Infrastructure',
    'Observable Graphics',
    'Scalable Services',
    'Maintainable Toolbox',
    'Composable Modules',
    'Controllable FOSS',
    'Affordable Solution',
  ];

  return (
    <div
      id="why-interactive"
      className="flex flex-col-reverse gap-3 md:flex-row md:min-h-[380px]"
    >
      <div className="flex flex-col">
        {items.map((item, i) => (
          <button
            key={item}
            ref={(element) => {
              if (!element || i !== active) return;

              scrollIntoView(element, {
                behavior: 'smooth',
                boundary: document.getElementById('why-interactive'),
              });
            }}
            type="button"
            className={cn(
              'transition-colors text-nowrap border border-transparent rounded-lg px-3 py-2.5 text-start text-sm text-fd-muted-foreground font-medium',
              i === active
                ? 'text-fd-primary bg-fd-primary/10 border-fd-primary/10'
                : 'hover:text-fd-accent-foreground/80',
            )}
            onClick={() => {
              setActive(i);
            }}
          >
            {item}
          </button>
        ))}
      </div>
      <style>
        {`
        @keyframes why-interactive-x {
          from {
            width: 0px;
          }

          to {
            width: 100%;
          }
        }`}
      </style>

      <div className="flex-1 p-4 border border-fd-primary/10 bg-fd-card/40 rounded-lg shadow-lg">
        {active === 0 ? (
          <WhyPanel>
            <h3>Blossom of Possibilities</h3>
            <p>Nurturing all, thriving in synergy, forging infinite possibilities!</p>
            <Cards>
              <Card title="Analytics" href="/docs/analytics">Big Data&apos;s new challenger</Card>
              <Card title="AI Ready" href="/docs/ai">Baseline for RAG/vector app</Card>
              <Card title="Geospatial" href="/docs/gis">De facto GIS standard</Card>
              <Card title="Time Series" href="/docs/timeseries">Temporal data mastery</Card>
              <Card title="Extensibility" href="/docs/extension">A Universe of Possibilities</Card>
              <Card title="Text Search" href="/docs/textsearch">Built-in search engine</Card>
              <Card title="Languages" href="/docs/language">Language of your choice</Card>
              <Card title="FDW Federation" href="/docs/fdw">Connecting data silos</Card>
            </Cards>
          </WhyPanel>
        ) : null}

        {active === 1 ? (
          <WhyPanel>
            <h3>Rock-Solid and Secure</h3>
            <p>Towering peaks, bedrock solid, standing firm at any summit!</p>
            <Cards>
              <Card title="High-Availability" href="/docs/ha">HA PostgreSQL</Card>
              <Card title="Self-Healing" href="/docs/ha">Adaptive service failover</Card>
              <Card title="PITR Protection" href="/docs/pitr">Auto-configured point-in-time recovery</Card>
              <Card title="Infra Closure" href="/docs/infra">No external dependencies</Card>
              <Card title="Access Control" href="/docs/security">Built-in best-practice model</Card>
              <Card title="Confidentiality" href="/docs/security">Guaranteed data security</Card>
              <Card title="Data Integrity" href="/docs/security">Thorough verification</Card>
              <Card title="Battle-Tested" href="/docs/benchmark">Availability benchmark</Card>
            </Cards>
          </WhyPanel>
        ) : null}

        {active === 2 ? (
          <WhyPanel>
            <h3>Clarity and Vision</h3>
            <p>Sky&apos;s movement, all-seeing view, perceiving details to master the whole!</p>
            <Cards>
              <Card title="Monitoring Infra" href="/docs/monitor">Built-in monitoring infrastructure</Card>
              <Card title="Data-Driven" href="/docs/monitor">Foundation for digital transformation</Card>
              <Card title="Ultimate Experience" href="/docs/monitor">The definitive Postgres monitoring solution</Card>
              <Card title="Universal Monitoring" href="/docs/monitor">Not limited to PG or RDS monitor</Card>
              <Card title="Automatic Alerts" href="/docs/monitor">No more manual checks</Card>
              <Card title="Performance Tuning" href="/docs/monitor">Slow-query bottlenecks uncovered</Card>
              <Card title="Logging Analysis" href="/docs/monitor">Fast root-cause detection</Card>
              <Card title="Custom Dashboards" href="/docs/monitor">Low-code visualization development</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 3 ? (
          <WhyPanel>
            <h3>Elastic Performance</h3>
            <p>Flowing like water, soft yet resilient, converging to adapt to endless change!</p>
            <Cards>
              <Card title="Blazing Performance" href="/docs/performance">New hardware fully harnessed</Card>
              <Card title="R/W Separation" href="/docs/performance">Unlimited read scaling</Card>
              <Card title="Connection Pooling" href="/docs/performance">High concurrency made easy</Card>
              <Card title="Load Balancing" href="/docs/performance">Console-driven traffic control</Card>
              <Card title="Horizontal Scaling" href="/docs/performance">In-place switch to distributed</Card>
              <Card title="Disk Expansion" href="/docs/performance">External tables with transparent compression</Card>
              <Card title="Mass Deployment" href="/docs/performance">Large clusters made easy</Card>
              <Card title="Cloud Elasticity" href="/docs/performance">Cloud-like elasticity</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 4 ? (
          <WhyPanel>
            <h3>Simple & Actionable</h3>
            <p>Blazing like wildfire, illuminating all around—true to the core while constantly innovating, burning bright without end!</p>
            <Cards>
              <Card title="Infra as Code" href="/docs/infra">Define and manage everything in code</Card>
              <Card title="Simple & Easy" href="/docs/infra">Up and running in minutes</Card>
              <Card title="Bare Linux" href="/docs/infra">No containers or K8s required</Card>
              <Card title="Offline Install" href="/docs/infra">Stable, hassle-free delivery</Card>
              <Card title="Admin SOP" href="/docs/infra">Best practices included</Card>
              <Card title="No Downtime" href="/docs/infra">Online migration and resizing</Card>
              <Card title="Rich Parameters" href="/docs/infra">Plenty of tunable parameters</Card>
              <Card title="Provisioning" href="/docs/infra">One-click server provisioning</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 5 ? (
          <WhyPanel>
            <h3>Flexible Building Blocks</h3>
            <p>Swift as the wind, simplifying complexity—riding the currents of change with freedom and ease!</p>
            <Cards>
              <Card title="Modular Design" href="/docs/module">Lego-like assembly</Card>
              <Card title="App Templates" href="/docs/module">One-click enterprise deployment</Card>
              <Card title="Core Modules" href="/docs/module">Fully-featured Postgres RDS</Card>
              <Card title="Extra Modules" href="/docs/module">Push the capability boundary</Card>
              <Card title="Kernel Modules" href="/docs/module">Swappable database engines</Card>
              <Card title="OLAP Modules" href="/docs/module">Powerful analytics capabilities</Card>
              <Card title="Pilot Modules" href="/docs/module">Exploring cutting-edge frontiers</Card>
              <Card title="Flavor Modules" href="/docs/module">Creative Postgres flavors</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 6 ? (
          <WhyPanel>
            <h3>Sovereign Self-Hosting</h3>
            <p>Grounded like the earth, gathering all rivers—standing firm while gazing at the stars!</p>
            <Cards>
              <Card title="Software Freedom" href="/docs/foss">Local-First OSS</Card>
              <Card title="No Vendor Lock-In" href="/docs/foss">Free Extension</Card>
              <Card title="Data Ownership" href="/docs/foss">Truly under your control</Card>
              <Card title="Friendly License" href="/docs/foss">Compliance Ready</Card>
              <Card title="Expert Support" href="/docs/foss">Top experts backing you</Card>
              <Card title="Self-hosting" href="/docs/foss">Democratized</Card>
              <Card title="Multi-Cloud" href="/docs/foss">No vendor lock-in</Card>
              <Card title="DIY Development" href="/docs/foss">Roll up your sleeves and build</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 7 ? (
          <WhyPanel>
            <h3>Cost-Effective RDS</h3>
            <p>Thunderous impact, breaking to build anew—keeping costs manageable and value ever rising!</p>
            <Cards>
              <Card title="No License Fee" href="/docs/afford">Do Less, Save More</Card>
              <Card title="DBA Efficiency" href="/docs/afford">Simple Architecture</Card>
              <Card title="Enable Cloud-Exit" href="/docs/afford">Key blockers resolved</Card>
              <Card title="Community Support" href="/docs/afford">Discuss, share, and co-create</Card>
              <Card title="Expert Consulting" href="/docs/afford">Expert help on demand</Card>
              <Card title="Commerical Support" href="/docs/afford">Transparent pricing, worth every penny</Card>
              <Card title="Open-Source" href="/docs/afford">Fully leverage PostgreSQL ecosystem</Card>
              <Card title="Save More" href="/docs/afford">Escape the RDS money pit</Card>
            </Cards>
          </WhyPanel>
        ) : null}
      </div>
    </div>
  );
}

function WhyPanel(props: HTMLProps<HTMLDivElement>) {
  return (
    <div
      {...props}
      className={cn(
        'duration-700 animate-in fade-in text-sm prose',
        props.className,
      )}
    >
      {props.children}
    </div>
  );
}

const previewButtonVariants = cva(
  'w-20 h-9 text-sm font-medium transition-colors rounded-full',
  {
    variants: {
      active: {
        true: 'text-fd-primary-foreground',
        false: 'text-fd-muted-foreground',
      },
    },
  },
);
export function PreviewImages() {
  const [active, setActive] = useState(0);

  return (
    <div className="mt-12 min-w-[800px] overflow-hidden xl:-mx-12 dark:[mask-image:linear-gradient(to_top,transparent,white_40px)]">
      <div className="absolute flex flex-row left-1/2 -translate-1/2 bottom-4 z-[2] p-1 rounded-full bg-fd-card border shadow-xl dark:shadow-fd-background">
        <div
          role="none"
          className="absolute bg-fd-primary rounded-full w-20 h-9 transition-transform z-[-1]"
          style={{
            transform: `translateX(calc(var(--spacing) * 20 * ${active}))`,
          }}
        />
        <button
          className={cn(previewButtonVariants({ active: active === 0 }))}
          onClick={() => setActive(0)}
        >
          Distro
        </button>
        <button
          className={cn(previewButtonVariants({ active: active === 1 }))}
          onClick={() => setActive(1)}
        >
          Panel
        </button>
        <button
            className={cn(previewButtonVariants({ active: active === 1 }))}
            onClick={() => setActive(2)}
        >
          Plugin
        </button>
      </div>
      <Image
        src={DistributionImg}
        alt="preview"
        priority
        className={cn(
          'w-full select-none duration-1000 animate-in fade-in -mb-60 slide-in-from-bottom-12 lg:-mb-40',
          active !== 0 && 'hidden',
        )}
      />
      {active === 1 && (
        <Image
          src={DashboardImg}
          alt="preview"
          priority
          className={cn(
            'w-full select-none duration-1000 animate-in fade-in -mb-60 slide-in-from-bottom-12 lg:-mb-40',
            active !== 1 && 'hidden',
          )}
        />
      )}
      {active === 2 && (
          <Image
              src={ExtensionImg}
              alt="Extensions"
              priority
              className={cn(
                  'w-full select-none duration-1000 animate-in fade-in -mb-60 slide-in-from-bottom-12 lg:-mb-40',
                  active !== 2 && 'hidden',
              )}
          />
      )}
    </div>
  );
}
