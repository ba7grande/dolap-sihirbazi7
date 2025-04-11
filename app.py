import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";

export default function Dashboard() {
  const [orders, setOrders] = useState([
    { id: 1, title: 'Mutfak Dolabı', status: 'Beklemede' },
    { id: 2, title: 'TV Ünitesi', status: 'Üretimde' },
  ]);

  const statuses = ['Beklemede', 'Üretimde', 'Tamamlandı', 'Teslim Edildi'];

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Üretim Paneli</h1>
      <Tabs defaultValue="Beklemede">
        <TabsList className="flex gap-2">
          {statuses.map((status) => (
            <TabsTrigger key={status} value={status}>{status}</TabsTrigger>
          ))}
        </TabsList>

        {statuses.map((status) => (
          <TabsContent key={status} value={status}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              {orders.filter(order => order.status === status).map(order => (
                <Card key={order.id}>
                  <CardContent className="p-4">
                    <h2 className="text-lg font-semibold">{order.title}</h2>
                    <p>Durum: {order.status}</p>
                    <Button
                      variant="outline"
                      className="mt-2"
                      onClick={() => {
                        const nextStatusIndex = (statuses.indexOf(order.status) + 1) % statuses.length;
                        const updatedOrders = orders.map(o => o.id === order.id ? { ...o, status: statuses[nextStatusIndex] } : o);
                        setOrders(updatedOrders);
                      }}
                    >
                      Durumu Güncelle
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
