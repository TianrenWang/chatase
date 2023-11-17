import { useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Icons } from "../../components/ui/icons";
import httpclient from "../../helpers/httpRequestClient";
import { Separator } from "../../components/ui/separator";

export default function APIKeysManager() {
  const [key, setKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  function generateAPIKey() {
    setIsLoading(true);

    httpclient
      .post("/api/apikey")
      .then((res) => {
        setKey(res.data.key);
      })
      .catch((error) => {
        console.log(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }

  return (
    <>
      <p className="text-sm text-muted-foreground">
        Click the button below to generate an API Key. Copy this API key and
        store it somewhere secure. We will never show you this API key again
        after you refresh this page.
      </p>
      <div className="flex space-x-2">
        <Input value={key} readOnly placeholder="API Key" />
        <Button
          disabled={isLoading}
          className="shrink-0"
          onClick={generateAPIKey}
        >
          {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />}
          Generate API Key
        </Button>
      </div>
      <h3 className="text-lg font-medium">How to use API key</h3>
      <Separator />
      <p className="text-sm text-muted-foreground">
        Add the API key to the "Authorization" header in your requests
      </p>
      <p className="text-sm text-muted-foreground">
        * Note: Because Chatase is currently a prototype, you can generate as
        many API keys as you want. However, they all authenticate to your, and
        each account can only support one conversational instance (for now).
      </p>
    </>
  );
}
