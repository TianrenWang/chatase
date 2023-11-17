import { Separator } from "../../components/ui/separator";

interface TabProps {
  children: React.ReactNode;
  tabDescription: string;
  tabTitle: string;
}

export default function TabWithHeader({
  children,
  tabDescription,
  tabTitle,
}: TabProps) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">{tabTitle}</h3>
        <p className="text-sm text-muted-foreground">{tabDescription}</p>
      </div>
      <Separator />
      {children}
    </div>
  );
}
