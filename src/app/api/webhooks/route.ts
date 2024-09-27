import { Webhook, WebhookRequiredHeaders } from "svix";
import { headers } from "next/headers";
import { WebhookEvent } from "@clerk/nextjs/server";
import { prisma } from "@/lib/db";
import { IncomingHttpHeaders } from "http";
import { NextResponse } from "next/server";

const webhookSecret = process.env.WEBHOOK_SECRET || "";

async function handler(req: Request) {
  console.log("inside webhook");
  const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET;

  if (!WEBHOOK_SECRET) {
    return NextResponse.json(
      {
        error:
          "Please add WEBHOOK_SECRET from Clerk Dashboard to .env or .env.local",
      },
      { status: 500 },
    );
  }

  const payload = await req.json();
  const headersList = headers();
  const heads = {
    "svix-id": headersList.get("svix-id"),
    "svix-timestamp": headersList.get("svix-timestamp"),
    "svix-signature": headersList.get("svix-signature"),
  };
  const wh = new Webhook(webhookSecret);
  let evt: Event | null = null;

  try {
    evt = wh.verify(
      JSON.stringify(payload),
      heads as IncomingHttpHeaders & WebhookRequiredHeaders,
    ) as Event;
  } catch (err) {
    console.error((err as Error).message);
    return NextResponse.json(
      { error: "Webhook verification failed" },
      { status: 400 },
    );
  }

  const eventType: EventType = evt.type;
  if (eventType === "user.created" || eventType === "user.updated") {
    const { id, ...attributes } = evt.data;

    try {
      await prisma.user.upsert({
        where: { externalId: id as string },
        create: {
          externalId: id as string,
          attributes,
        },
        update: { attributes },
      });
    } catch (error) {
      console.error("Database error:", error);
      return NextResponse.json({ error: "Database error" }, { status: 500 });
    }
  }

  // Return a success response
  return NextResponse.json(
    { message: "Webhook processed successfully" },
    { status: 200 },
  );
}

type EventType = "user.created" | "user.updated" | "*";

type Event = {
  data: Record<string, string | number>;
  object: "event";
  type: EventType;
};

export const GET = handler;
export const POST = handler;
export const PUT = handler;
