import { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { API_BASE_URL } from './src/config/api';

type MenuItem = {
  id: number;
  name: string;
  price_cents: number;
};

function toUSD(priceCents: number): string {
  return `$${(priceCents / 100).toFixed(2)}`;
}

export default function App() {
  const [items, setItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadMenu() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/menu`);
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const data = (await response.json()) as MenuItem[];
        if (isMounted) {
          setItems(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Failed to fetch menu.');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    loadMenu();
    return () => {
      isMounted = false;
    };
  }, []);

  const emptyMessage = useMemo(() => (!loading && !error && items.length === 0 ? 'No items yet' : null), [error, items.length, loading]);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Menu</Text>

      {loading && (
        <View style={styles.centered}>
          <ActivityIndicator size="large" />
          <Text style={styles.secondaryText}>Loading menu...</Text>
        </View>
      )}

      {!loading && error && (
        <View style={styles.centered}>
          <Text style={styles.errorText}>Error: {error}</Text>
        </View>
      )}

      {!loading && !error && (
        <FlatList
          data={items}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={items.length === 0 ? styles.centeredList : undefined}
          ListEmptyComponent={<Text style={styles.secondaryText}>{emptyMessage}</Text>}
          renderItem={({ item }) => (
            <View style={styles.row}>
              <Text style={styles.itemName}>{item.name}</Text>
              <Text style={styles.itemPrice}>{toUSD(item.price_cents)}</Text>
            </View>
          )}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingTop: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 12,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  centeredList: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  secondaryText: {
    color: '#666',
    fontSize: 16,
  },
  errorText: {
    color: '#c00',
    fontSize: 16,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  itemName: {
    fontSize: 18,
  },
  itemPrice: {
    fontSize: 18,
    fontWeight: '600',
  },
});
