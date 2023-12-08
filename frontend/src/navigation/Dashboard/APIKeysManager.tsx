import { useEffect, useRef, useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Icons } from "../../components/ui/icons";
import httpclient from "../../helpers/httpRequestClient";
import { Separator } from "../../components/ui/separator";
import { Textarea } from "../../components/ui/textarea";

export default function APIKeysManager() {
  const [key, setKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState("");
  const [isLoadingMessage, setIsLoadingMessage] = useState(false);
  const textingBox = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textingBox.current)
      textingBox.current.scrollTop = textingBox.current.scrollHeight;
  }, [messages]);

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

  function sendMessage() {
    setIsLoadingMessage(true);
    setMessages((currentMessages) => {
      return currentMessages + `You: ${message}\n`;
    });
    setMessage("");

    const convoIdCache = localStorage.getItem("conversationId");

    const config = convoIdCache
      ? { params: { conversationId: convoIdCache } }
      : {};

    httpclient
      .post("/api/test_chat", { text: message }, config)
      .then((res) => {
        if (!convoIdCache)
          localStorage.setItem("conversationId", res.data.conversationId);

        setMessages((currentMessages) => {
          return currentMessages + `Sophia: ${res.data.message}\n`;
        });
      })
      .catch((error) => {
        console.log(error.message);
      })
      .finally(() => {
        setIsLoadingMessage(false);
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
      <p className="text-sm text-muted-foreground">
        * Note: Because Chatase is currently a prototype, you can generate as
        many API keys as you want. However, they all authenticate to you, and
        each account can only support one conversational instance (for now).
      </p>
      <h3 className="text-lg font-medium">Test the API</h3>
      <Separator />
      <p className="text-sm text-muted-foreground">
        Send messages to the chatbot to get an idea of how it works (it
        remembers your past messages).
      </p>
      <div className="flex space-x-2">
        <Input
          disabled={isLoadingMessage}
          value={message}
          onChange={(event) => {
            setMessage(event.target.value);
          }}
          placeholder="Type your test message here"
        />
        <Button
          disabled={!message || isLoadingMessage}
          className="shrink-0"
          onClick={sendMessage}
        >
          {isLoadingMessage && (
            <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
          )}
          Send Message
        </Button>
      </div>
      <Textarea
        value={messages}
        readOnly
        placeholder={
          "Your text messages will appear here.\nContext: You are texting Sophia, your girlfriend."
        }
        className="resize-none min-h-[200px]"
        ref={textingBox}
      />
      <h3 className="text-lg font-medium">Usage Instruction</h3>
      <Separator />
      <p className="text-sm text-muted-foreground">
        The way this service works is that users can chat with a chatbot
        girlfriend called Sophia. To do so, you must first create an instance of
        Conversation, and then you can start sending and receiving messages from
        it. To create a conversation, send a <code>POST</code> request to{" "}
        <code>/api/chat</code> to get the ID of the conversation. To send and
        receive messsages, send a <code>GET</code> request to{" "}
        <code>/api/chat?conversationId=your_conversationId</code> with{" "}
        <code>{'{ text: "<arbitrary_text_message>" }'}</code> as the body. Keep
        in mind that all of these requests require you to add the <b>API key</b>{" "}
        to the Authorization header as a Bearer token.
      </p>
      <p className="text-sm text-muted-foreground">
        It is important to note that this service only retain past messages to
        optimize the performance of the bot responses. Do not rely on this
        service to track your conversation history.
      </p>
    </>
  );
}
