import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { toast } from "../../components/ui/use-toast";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../../components/ui/form";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";
import { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import httpclient from "../../helpers/httpRequestClient";

const accountFormSchema = z
  .object({
    email: z.string().email(),
  })
  .required();

type AccountFormValues = z.infer<typeof accountFormSchema>;

export default function AccountForm() {
  const { user, setUser } = useContext(AuthContext);
  const form = useForm<AccountFormValues>({
    resolver: zodResolver(accountFormSchema),
    defaultValues: { email: user?.email || "" },
  });

  function onSubmit(data: AccountFormValues) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  function submitLogout(e: React.FormEvent) {
    e.preventDefault();
    httpclient.post("/api/logout", { withCredentials: true }).then(() => {
      setUser(undefined);
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input readOnly {...field} />
              </FormControl>
              <FormDescription>
                {"You currently cannot modify your email. Sorry :("}
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        {/* <Button type="submit">Update account</Button> */}
      </form>
      <Button variant="destructive" onClick={submitLogout}>
        Logout
      </Button>
    </Form>
  );
}
