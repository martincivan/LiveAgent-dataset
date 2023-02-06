from liveagent_api import GridApi, TicketsApi
from my_client import client


def get_tickets(cursor: str = ""):
    api = GridApi(api_client=client)
    data = api.get_tickets_grid_list_with_http_info(per_page=500, sort_dir="DESC",
                                                    filters="[[\"rstatus\",\"IN\",\"A,P,T,N,C,R,W\"],[\"channel_type\",\"IN\",\"B,M,E,F,A,I,Q,S,C,W,T\"]]",
                                                    cursor=cursor, sort_field="datechanged")
    yield from data[0]
    try:
        cursor = data[2]["next_page_cursor"]
        if cursor:
            yield from get_tickets(cursor=cursor)
    except KeyError:
        pass


def get_groups(id: str, _from: int = 0):
    api = TicketsApi(api_client=client)
    per_page = 500
    data = api.get_ticket_message_groups(ticket_id=id, include_quoted_messages=False, _from=_from, to=_from+per_page)
    yield from data
    if len(data) == per_page:
        yield from get_groups(id, _from=_from+len(data))



if __name__ == "__main__":
    i = 0
    for ticket in get_tickets():
        i+=1
        print(i)
        print("TICKET: " + ticket.conversationid + "############################")
        for group in get_groups(ticket.conversationid):
            for message in group.messages:
                if message.message:
                    print(message.message[:50])