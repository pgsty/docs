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
import Link from 'next/link';

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
    <Link href="/docs/install/interface">
      <div
      {...props}
      className={cn(
        'overflow-hidden rounded-md border bg-fd-background shadow-xl',
        props.className,
      )}
    >
      <div className="relative flex h-6 flex-row items-center border-b bg-fd-muted px-4 text-xs text-fd-muted-foreground">
        <p className="absolute inset-x-0 text-center">grafana @ :3000</p>
      </div>
      <div className="p-4 text-sm"><code>admin:pigsty</code></div>
    </div></Link>
  );
}

export function WhyInteractive() {
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
      className="flex flex-col-reverse gap-6 md:flex-row md:min-h-[380px]"
    >
      <div className="flex flex-col md:w-80 md:flex-shrink-0">
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
              'transition-colors text-nowrap border border-transparent rounded-lg px-4 py-4 text-center text-base text-fd-muted-foreground font-semibold flex-1',
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
              <Card title="Analytics" href="/docs/value/extensibility#analytics">OLAP&apos;s new challenger</Card>
              <Card title="AI Ready" href="/docs/value/extensibility#ai-ready">RAG / Vector Defaults</Card>
              <Card title="Geospatial" href="/docs/value/extensibility#geospatial">De facto GIS standard</Card>
              <Card title="Time Series" href="/docs/value/extensibility#time-series">Temporal data mastery</Card>
              <Card title="Featured" href="/docs/value/extensibility#featured">Database as a Platform</Card>
              <Card title="Full-Text Search" href="/docs/value/extensibility#text-search">Built-in search engine</Card>
              <Card title="PL Languages" href="/docs/value/extensibility#languages">Procedure Language</Card>
              <Card title="FDW Federation" href="/docs/value/extensibility#foreign-data">Connecting data silos</Card>
            </Cards>
          </WhyPanel>
        ) : null}

        {active === 1 ? (
          <WhyPanel>
            <h3>Rock-Solid and Secure</h3>
            <p>Towering peaks, bedrock solid, standing firm at any summit!</p>
            <Cards>
              <Card title="High-Availability" href="/docs/value/reliability#high-availability">Reliable PostgreSQL RDS</Card>
              <Card title="Self-Healing" href="/docs/value/reliability#self-healing">Adaptive service failover</Card>
              <Card title="PITR Protection" href="/docs/value/reliability#pitr-protection">Pre-configured Backup & Archives</Card>
              <Card title="Infra Closure" href="/docs/value/reliability#infra-closure">No external dependencies</Card>
              <Card title="Access Control" href="/docs/value/reliability#access-control">Built-in best-practice model</Card>
              <Card title="Confidentiality" href="/docs/value/reliability#confidentiality">Guaranteed data security</Card>
              <Card title="Data Integrity" href="/docs/value/reliability#data-integrity">Thorough verification</Card>
              <Card title="Battle-Tested" href="/docs/value/reliability#battle-tested">Availability Results</Card>
            </Cards>
          </WhyPanel>
        ) : null}

        {active === 2 ? (
          <WhyPanel>
            <h3>Clarity and Vision</h3>
            <p>Sky&apos;s movement, all-seeing view, perceiving details to master the whole!</p>
            <Cards>
              <Card title="Monitoring Infra" href="/docs/value/observability#monitoring-infra">Built-in Observability Stack</Card>
              <Card title="Data-Driven" href="/docs/value/observability#data-driven">Measure what you Manage</Card>
              <Card title="SOTA Experience" href="/docs/value/observability#sota-experience">The Definitive PG monitoring</Card>
              <Card title="Universal Monitoring" href="/docs/value/observability#universal-monitoring">RDS or Compat Kernels</Card>
              <Card title="Automatic Alerts" href="/docs/value/observability#automatic-alerts">No more manual checks</Card>
              <Card title="Performance Tuning" href="/docs/value/observability#performance-tuning">Slow-query Optimize</Card>
              <Card title="Log Analysis" href="/docs/value/observability#log-analysis">Fast root-cause detection</Card>
              <Card title="Custom Dashboards" href="/docs/value/observability#custom-dashboards">Low-code Data App</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 3 ? (
          <WhyPanel>
            <h3>Elastic Performance</h3>
            <p>Flowing like water, soft yet resilient, converging to adapt to endless change!</p>
            <Cards>
              <Card title="Great Performance" href="/docs/value/scalability#great-performance">Hardware Fully Harnessed</Card>
              <Card title="R/W Separation" href="/docs/value/scalability#rw-separation">Unlimited Read Scaling</Card>
              <Card title="Connection Pooling" href="/docs/value/scalability#connection-pooling">High Concurrency</Card>
              <Card title="Load Balancing" href="/docs/value/scalability#load-balancing">Traffic Control</Card>
              <Card title="Horizontal Scaling" href="/docs/value/scalability#horizontal-scaling">Distributive Extension</Card>
              <Card title="Storage Expansion" href="/docs/value/scalability#storage-expansion">Transparent Compression</Card>
              <Card title="Mass Deployment" href="/docs/value/scalability#mass-deployment">Large clusters made easy</Card>
              <Card title="Elasticity" href="/docs/value/scalability#elasticity">Cloud-like Elasticity</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 4 ? (
          <WhyPanel>
            <h3>Simple & Actionable</h3>
            <p>Blazing like wildfire, illuminating all around — constantly evolving and burning bright without end!</p>
            <Cards>
              <Card title="Infra as Code" href="/docs/value/maintainability#infra-as-code">Define everything in Code</Card>
              <Card title="Simple & Easy" href="/docs/value/maintainability#simple-easy">Up and Running in Minutes</Card>
              <Card title="Bare Linux" href="/docs/value/maintainability#bare-linux">No Containers or Kubernetes</Card>
              <Card title="Offline Install" href="/docs/value/maintainability#offline-install">Stable, Hassle-free Delivery</Card>
              <Card title="Admin SOP" href="/docs/value/maintainability#admin-sop">Best Practices Included</Card>
              <Card title="No Downtime" href="/docs/value/maintainability#no-downtime">Online Migration & Resizing</Card>
              <Card title="Rich Parameters" href="/docs/value/maintainability#rich-parameters">Plenty of Tunable Knobs</Card>
              <Card title="Provisioning" href="/docs/value/maintainability#provisioning">One-command IaaS Provisioning</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 5 ? (
          <WhyPanel>
            <h3>Flexible Building Blocks</h3>
            <p>Swift as the wind, simplifying complexity—riding the currents of change with freedom and ease!</p>
            <Cards>
              <Card title="Modular Design" href="/docs/value/composability#modular-design">Lego-like Assembly</Card>
              <Card title="App Templates" href="/docs/value/composability#app-templates">One-Click Enterprise Deployment</Card>
              <Card title="Core Modules" href="/docs/value/composability#core-modules">Fully-Featured Postgres RDS</Card>
              <Card title="Extra Modules" href="/docs/value/composability#extra-modules">Extending RDS Capabilities</Card>
              <Card title="Kernel Modules" href="/docs/value/composability#kernel-modules">Swappable Database Engines</Card>
              <Card title="OLAP Modules" href="/docs/value/composability#olap-modules">Powerful Analytics Capabilities</Card>
              <Card title="Pilot Modules" href="/docs/value/composability#pilot-modules">Exploring Cutting-Edge Frontiers</Card>
              <Card title="Flavor Modules" href="/docs/value/composability#flavor-modules">Creative Postgres Flavors</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 6 ? (
          <WhyPanel>
            <h3>Sovereign Self-Hosting</h3>
            <p>Grounded like the earth, gathering all rivers—standing firm while gazing at the stars!</p>
            <Cards>
              <Card title="Software Freedom" href="/docs/value/controllability#software-freedom">Self-hosting democratized</Card>
              <Card title="Local-First" href="/docs/value/controllability#local-first">Run on-premises indefinitely</Card>
              <Card title="Multi-Cloud" href="/docs/value/controllability#multi-cloud">No vendor lock-in</Card>
              <Card title="Free Extensions" href="/docs/value/controllability#free-extensions">420+ PostgreSQL extensions</Card>
              <Card title="Data Ownership" href="/docs/value/controllability#data-ownership">Pay fair cost for resources</Card>
              <Card title="Friendly License" href="/docs/value/controllability#friendly-license">AGPLv3 preserving freedom</Card>
              <Card title="Compliance Ready" href="/docs/value/controllability#compliance-ready">Meeting domestic requirements</Card>
              <Card title="Expert Support" href="/docs/value/controllability#expert-support">Top-tier PostgreSQL specialists</Card>
            </Cards>
          </WhyPanel>
        ) : null}
        {active === 7 ? (
          <WhyPanel>
            <h3>Cost-Effective RDS</h3>
            <p>Thunderous impact, breaking to build anew—keeping costs manageable and value ever rising!</p>
            <Cards>
              <Card title="Open-Source" href="/docs/value/affordability#open-source">Fully leverage PostgreSQL's eco</Card>
              <Card title="Save More" href="/docs/value/affordability#save-more">Escape the RDS money pit</Card>
              <Card title="DBA Efficiency" href="/docs/value/affordability#dba-efficiency">Everyone can be a DBA</Card>
              <Card title="Simplified Arch" href="/docs/value/affordability#simplified-arch">No Containers or K8s</Card>
              <Card title="Enable Cloud-Exit" href="/docs/value/affordability#cloud-exit">Key blockers resolved</Card>
              <Card title="Community Support" href="/docs/value/affordability#community-support">Discuss & Share</Card>
              <Card title="Expert Consultation" href="/docs/value/affordability#expert-consult">Pay as needed</Card>
              <Card title="Subscription" href="/docs/value/affordability#subscription">Clear pricing, value for money</Card>
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
