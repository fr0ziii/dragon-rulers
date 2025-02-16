"use client"

import * as React from "react"
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
  Home,
  Component,
  ChartArea,
  Speech,
  Link
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { getAgents } from "@/lib/api"; // Import the API function
import { Collapsible } from "@radix-ui/react-collapsible"

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Acme Inc",
      logo: GalleryVerticalEnd,
      plan: "Enterprise",
    },
    {
      name: "Acme Corp.",
      logo: AudioWaveform,
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: Command,
      plan: "Free",
    },
  ],
   navMain: [ // Remove static navMain
     {
       title: "Home",
       url: "#",
       icon: Home,
       Collapsible: false,
       isActive: true,
       items: [
         {
           title: "Dashboard",
           url: "/dashboard",
         },
       ],
     },
     {
       title: "Models",
       url: "#",
       icon: Component,
       items: [
         {
           title: "Agents",
           url: "#",
           icon: Bot,
         },
         {
           title: "Strategies",
           url: "#",
           icon: ChartArea
         },
         {
           title: "Swarms",
           url: "#",
           icon: Speech
         },
         {
          title: "Blockchains",
          url: "#",
          icon: Link
        },
       ],
     },
   ],
  projects: [
    {
      name: "Design Engineering",
      url: "#",
      icon: Frame,
    },
    {
      name: "Sales & Marketing",
      url: "#",
      icon: PieChart,
    },
    {
      name: "Travel",
      url: "#",
      icon: Map,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const [navItems, setNavItems] = React.useState([]);

  React.useEffect(() => {
    const fetchNavData = async () => {
      try {
        const agents = await getAgents();
        // Transform agents data to fit NavMain's expected structure
        const transformedNavItems = agents.map((agent: { name: any; id: any; }) => ({
          title: agent.name,
          url: `/agent/${agent.id}`, // Example URL
          // icon: SquareTerminal, // You might need a mapping for icons
        }));
        setNavItems(transformedNavItems);
      } catch (error) {
        console.error("Failed to fetch navigation data:", error);
        // Handle error appropriately
      }
    };

    fetchNavData();
  }, []);

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        { <NavMain items={data.navMain} /> }
        <NavMain items={navItems} />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
