import { Webhook, WebhookRequiredHeaders } from "svix";
import { headers } from "next/headers";
import { prisma } from "@/lib/db";
import { IncomingHttpHeaders } from "http";
import { NextResponse } from "next/server";
import { User, WebhookEvent } from "@clerk/nextjs/server"; // Assuming this gives types
console.log("hi i am here");

const webhookSecret = process.env.WEBHOOK_SECRET || "";

async function handler(req: Request) {
  console.log("inside webhook");

  if (!webhookSecret) {
    return NextResponse.json(
      { error: "Please add WEBHOOK_SECRET to .env or .env.local" },
      { status: 500 },
    );
  }

  const payload = await req.json();
  const headersList = headers();

  const heads = {
    "svix-id": headersList.get("svix-id") || "",
    "svix-timestamp": headersList.get("svix-timestamp") || "",
    "svix-signature": headersList.get("svix-signature") || "",
  };

  const wh = new Webhook(webhookSecret);
  let evt: Event | null = null;

  try {
    evt = wh.verify(
      JSON.stringify(payload),
      heads as IncomingHttpHeaders & WebhookRequiredHeaders,
    ) as Event;
  } catch (err) {
    console.error("Webhook verification error:", (err as Error).message);
    return NextResponse.json(
      { error: "Webhook verification failed" },
      { status: 400 },
    );
  }

  const eventType: EventType = evt.type;

  if (
    eventType === "user.created" ||
    eventType === "user.updated" ||
    eventType === "*"
  ) {
    const { id, ...attributes } = evt.data;

    try {
      // Check if the user already exists
      const existingUser = await prisma.user.findUnique({
        where: { externalId: id as string },
      });

      if (existingUser) {
        console.log("Existing user:", existingUser.attributes?.valueOf());
        return NextResponse.json(
          { message: `User already exists: ${existingUser.externalId}` },
          { status: 200 },
        );
      }

      // If user doesn't exist, proceed with the upsert
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
      return NextResponse.json(
        { error: "Database operation failed" },
        { status: 500 },
      );
    }
  }

  return NextResponse.json(
    { message: "Webhook processed successfully" },
    { status: 200 },
  );
}

// Event Types
type EventType = "user.created" | "user.updated";

type Event = {
  data: Record<string, any>; // Clerk data can vary, might use 'any' here
  object: "event";
  type: EventType;
};

// Export handlers for different HTTP methods
export const GET = handler;
export const POST = handler;
export const PUT = handler;
