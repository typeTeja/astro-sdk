# AstroSDK API Documentation for Next.js

> Auto-generated documentation for the AstroSDK 2.0 API routes. These endpoints map perfectly to App Router React Server Components.

## 1. Check ephemeris loaded state

- **Method:** `GET`
- **Path:** `/api/v2/astro/ephemeris-status`
- **Description:** Check ephemeris loaded state

### Request Example

No parameters required

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/astro/ephemeris-status');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 2. Get Settings

- **Method:** `GET`
- **Path:** `/api/v2/astro/settings`
- **Description:** Get Settings

### Request Example

No parameters required

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/astro/settings');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 3. Validate Settings

- **Method:** `POST`
- **Path:** `/api/v2/astro/settings`
- **Description:** Validate Settings

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/astro/settings', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 4. Generate full natal chart

- **Method:** `POST`
- **Path:** `/api/v2/charts/natal`
- **Description:** Generate full natal chart

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/charts/natal', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 5. Get current transit chart

- **Method:** `GET`
- **Path:** `/api/v2/charts/transits`
- **Description:** Get current transit chart

### Request Example

`?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/charts/transits' + '?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 6. Calculate Panchanga

- **Method:** `GET`
- **Path:** `/api/v2/charts/panchanga`
- **Description:** Calculate Panchanga

### Request Example

`?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/charts/panchanga' + '?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 7. Get sign ingresses for a planet

- **Method:** `GET`
- **Path:** `/api/v2/events/ingresses`
- **Description:** Get sign ingresses for a planet

### Request Example

`?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/events/ingresses' + '?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 8. Get planetary stations

- **Method:** `GET`
- **Path:** `/api/v2/events/retrogrades`
- **Description:** Get planetary stations

### Request Example

`?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/events/retrogrades' + '?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 9. Get major lunar phases

- **Method:** `GET`
- **Path:** `/api/v2/lunar/phases`
- **Description:** Get major lunar phases

### Request Example

`?start_time=value&count=value&angle=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/lunar/phases' + '?start_time=value&count=value&angle=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 10. Get lunar perigee and apogee

- **Method:** `GET`
- **Path:** `/api/v2/lunar/extremes`
- **Description:** Get lunar perigee and apogee

### Request Example

`?start_time=value&count=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/lunar/extremes' + '?start_time=value&count=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 11. Search for eclipses

- **Method:** `GET`
- **Path:** `/api/v2/lunar/eclipses`
- **Description:** Search for eclipses

### Request Example

`?start_time=value&count=value&solar=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/lunar/eclipses' + '?start_time=value&count=value&solar=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 12. Calculate aspects between objects

- **Method:** `GET`
- **Path:** `/api/v2/aspects/calculate`
- **Description:** Calculate aspects between objects

### Request Example

`?time=value&planets=value&aspect_types=value&global_orb=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/aspects/calculate' + '?time=value&planets=value&aspect_types=value&global_orb=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 13. Get secondary progression positions

- **Method:** `GET`
- **Path:** `/api/v2/progressions/secondary`
- **Description:** Get secondary progression positions

### Request Example

`?birth_time=value&target_date=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/progressions/secondary' + '?birth_time=value&target_date=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 14. Scan valid aspects between progressed planets and natal chart

- **Method:** `POST`
- **Path:** `/api/v2/progressions/aspects`
- **Description:** Scan valid aspects between progressed planets and natal chart

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/progressions/aspects', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 15. Get synodic cycle phase

- **Method:** `GET`
- **Path:** `/api/v2/quant/synodic/phase`
- **Description:** Get synodic cycle phase

### Request Example

`?p1=value&p2=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/quant/synodic/phase' + '?p1=value&p2=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 16. Find next synodic event

- **Method:** `GET`
- **Path:** `/api/v2/quant/synodic/next`
- **Description:** Find next synodic event

### Request Example

`?p1=value&p2=value&target_angle=value&time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/quant/synodic/next' + '?p1=value&p2=value&target_angle=value&time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 17. Get quantitative indicators

- **Method:** `GET`
- **Path:** `/api/v2/quant/indicators`
- **Description:** Get quantitative indicators

### Request Example

`?time=value&planets=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/quant/indicators' + '?time=value&planets=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 18. Scan for transits to a natal chart

- **Method:** `POST`
- **Path:** `/api/v2/transits/scan`
- **Description:** Scan for transits to a natal chart

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/transits/scan', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 19. Scan heliocentric transits

- **Method:** `POST`
- **Path:** `/api/v2/transits/helion`
- **Description:** Scan heliocentric transits

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/transits/helion', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 20. Scan for declination parallels

- **Method:** `POST`
- **Path:** `/api/v2/transits/declination`
- **Description:** Scan for declination parallels

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/transits/declination', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 21. Find the next planetary return to a given longitude

- **Method:** `GET`
- **Path:** `/api/v2/crossings/return`
- **Description:** Find the next planetary return to a given longitude

### Request Example

`?planet=value&target_longitude=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/crossings/return' + '?planet=value&target_longitude=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 22. Find exact inter-planetary aspect crossing

- **Method:** `GET`
- **Path:** `/api/v2/crossings/aspect`
- **Description:** Find exact inter-planetary aspect crossing

### Request Example

`?p1=value&p2=value&target_angle=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/crossings/aspect' + '?p1=value&p2=value&target_angle=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 23. Calculate rise, transit, and set times for a planet

- **Method:** `GET`
- **Path:** `/api/v2/horizon/rise-set`
- **Description:** Calculate rise, transit, and set times for a planet

### Request Example

`?planet=value&altitude=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/horizon/rise-set' + '?planet=value&altitude=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 24. Calculate civil, nautical, or astronomical twilight

- **Method:** `GET`
- **Path:** `/api/v2/horizon/twilight`
- **Description:** Calculate civil, nautical, or astronomical twilight

### Request Example

`?altitude=value&time=value&twilight_type=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/horizon/twilight' + '?altitude=value&time=value&twilight_type=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 25. Get position of a named fixed star

- **Method:** `GET`
- **Path:** `/api/v2/stars/{star_name}`
- **Description:** Get position of a named fixed star

### Request Example

`?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/stars/{star_name}' + '?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 26. Get positions of multiple named fixed stars

- **Method:** `GET`
- **Path:** `/api/v2/stars/`
- **Description:** Get positions of multiple named fixed stars

### Request Example

`?star_names=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/stars/' + '?star_names=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 27. Get North and South lunar node positions

- **Method:** `GET`
- **Path:** `/api/v2/nodes/lunar`
- **Description:** Get North and South lunar node positions

### Request Example

`?time=value&true_node=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/nodes/lunar' + '?time=value&true_node=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 28. Get Black Moon Lilith position

- **Method:** `GET`
- **Path:** `/api/v2/nodes/lilith`
- **Description:** Get Black Moon Lilith position

### Request Example

`?time=value&true_lilith=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/nodes/lilith' + '?time=value&true_lilith=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 29. Get nodes and apsides for a planet

- **Method:** `GET`
- **Path:** `/api/v2/nodes/planetary/{planet}`
- **Description:** Get nodes and apsides for a planet

### Request Example

`?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/nodes/planetary/{planet}' + '?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 30. Find parans for a given date and location

- **Method:** `GET`
- **Path:** `/api/v2/parans/`
- **Description:** Find parans for a given date and location

### Request Example

`?altitude=value&time=value&orb_minutes=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/parans/' + '?altitude=value&time=value&orb_minutes=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 31. Find the next heliacal rising of a planet or star

- **Method:** `GET`
- **Path:** `/api/v2/heliacal/rising`
- **Description:** Find the next heliacal rising of a planet or star

### Request Example

`?planet=value&altitude=value&time=value&star_name=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/heliacal/rising' + '?planet=value&altitude=value&time=value&star_name=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 32. Find the next heliacal setting of a planet or star

- **Method:** `GET`
- **Path:** `/api/v2/heliacal/setting`
- **Description:** Find the next heliacal setting of a planet or star

### Request Example

`?planet=value&altitude=value&time=value&star_name=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/heliacal/setting' + '?planet=value&altitude=value&time=value&star_name=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 33. Find all retrograde and direct stations for a planet in a year

- **Method:** `GET`
- **Path:** `/api/v2/heliacal/stations`
- **Description:** Find all retrograde and direct stations for a planet in a year

### Request Example

`?planet=value&year=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/heliacal/stations' + '?planet=value&year=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 34. Find the next exact synodic event between two planets

- **Method:** `GET`
- **Path:** `/api/v2/synodic/next`
- **Description:** Find the next exact synodic event between two planets

### Request Example

`?p1=value&p2=value&target_angle=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/synodic/next' + '?p1=value&p2=value&target_angle=value&start_time=value&max_days=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 35. Get bounded time windows like retrograde phases.

- **Method:** `GET`
- **Path:** `/api/v2/financial/time-windows`
- **Description:** Get bounded time windows like retrograde phases.

### Request Example

`?start_time=value&max_days=value&planets=value&preset=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/financial/time-windows' + '?start_time=value&max_days=value&planets=value&preset=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 36. Get Financial Retrogrades

- **Method:** `GET`
- **Path:** `/api/v2/financial/retrogrades`
- **Description:** Get Financial Retrogrades

### Request Example

`?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/financial/retrogrades' + '?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 37. Get Financial Ingresses

- **Method:** `GET`
- **Path:** `/api/v2/financial/ingresses`
- **Description:** Get Financial Ingresses

### Request Example

`?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/financial/ingresses' + '?planet=value&start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 38. Get Financial Eclipses

- **Method:** `GET`
- **Path:** `/api/v2/financial/eclipses`
- **Description:** Get Financial Eclipses

### Request Example

`?start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/financial/eclipses' + '?start_time=value&end_time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 39. Get Financial Events

- **Method:** `GET`
- **Path:** `/api/v2/financial/events`
- **Description:** Get Financial Events

### Request Example

`?start_time=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/financial/events' + '?start_time=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 40. Get rolling aspect intensity scores

- **Method:** `GET`
- **Path:** `/api/v2/signals/astro-intensity`
- **Description:** Get rolling aspect intensity scores

### Request Example

`?start_time=value&max_days=value&step_hours=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/signals/astro-intensity' + '?start_time=value&max_days=value&step_hours=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 41. Find planetary clusters (Stelliums)

- **Method:** `GET`
- **Path:** `/api/v2/signals/cluster-index`
- **Description:** Find planetary clusters (Stelliums)

### Request Example

`?start_time=value&max_days=value&step_hours=value&orb_degrees=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/signals/cluster-index' + '?start_time=value&max_days=value&step_hours=value&orb_degrees=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 42. [EXPERIMENTAL] Composite Centroid

- **Method:** `POST`
- **Path:** `/api/v2/cycles/composite`
- **Description:** [EXPERIMENTAL] Composite Centroid

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/cycles/composite', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 43. [EXPERIMENTAL] Time-Swing Projection

- **Method:** `GET`
- **Path:** `/api/v2/projections/time-swing`
- **Description:** [EXPERIMENTAL] Time-Swing Projection

### Request Example

`?start_time=value&interval_days=value&iterations=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/projections/time-swing' + '?start_time=value&interval_days=value&iterations=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 44. [EXPERIMENTAL] Synodical Lines Projection

- **Method:** `GET`
- **Path:** `/api/v2/projections/synodical-lines`
- **Description:** [EXPERIMENTAL] Synodical Lines Projection

### Request Example

`?planet=value&start_time=value&interval_degrees=value&iterations=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/projections/synodical-lines' + '?planet=value&start_time=value&interval_degrees=value&iterations=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 45. [V2] Get single planet position

- **Method:** `GET`
- **Path:** `/api/v2/astronomy/planet-position`
- **Description:** [V2] Get single planet position

### Request Example

`?planet=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/astronomy/planet-position' + '?planet=value&time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 46. [V2] Generate full natal chart

- **Method:** `POST`
- **Path:** `/api/v2/western/natal`
- **Description:** [V2] Generate full natal chart

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/western/natal', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 47. [V2] Get transit chart

- **Method:** `GET`
- **Path:** `/api/v2/western/transits`
- **Description:** [V2] Get transit chart

### Request Example

`?time=value&latitude=value&longitude=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/western/transits' + '?time=value&latitude=value&longitude=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 48. [V2] Get Vedic Panchang

- **Method:** `GET`
- **Path:** `/api/v2/vedic/panchang`
- **Description:** [V2] Get Vedic Panchang

### Request Example

`?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/vedic/panchang' + '?time=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 49. Calculate a varga (divisional chart)

- **Method:** `POST`
- **Path:** `/api/v2/vedic/classic/divisional`
- **Description:** Calculate a varga (divisional chart)

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/vedic/classic/divisional', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 50. Calculate predictive dasha periods

- **Method:** `POST`
- **Path:** `/api/v2/vedic/classic/dashas`
- **Description:** Calculate predictive dasha periods

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/vedic/classic/dashas', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 51. [EXPERIMENTAL] Shadbala Planetary Strength

- **Method:** `POST`
- **Path:** `/api/v2/vedic/classic/shadbala`
- **Description:** [EXPERIMENTAL] Shadbala Planetary Strength

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/vedic/classic/shadbala', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 52. [EXPERIMENTAL] Ashtakavarga Array

- **Method:** `POST`
- **Path:** `/api/v2/vedic/classic/ashtakavarga`
- **Description:** [EXPERIMENTAL] Ashtakavarga Array

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/vedic/classic/ashtakavarga', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 53. Stream bulk ephemeris data as CSV

- **Method:** `GET`
- **Path:** `/api/v2/research/ephemeris/csv`
- **Description:** Stream bulk ephemeris data as CSV

### Request Example

`?start_time=value&years=value&step_hours=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/research/ephemeris/csv' + '?start_time=value&years=value&step_hours=value&house_system=value&sidereal_mode=value&is_sidereal=value&coordinate_system=value&latitude=value&longitude=value&altitude=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 54. Post Astro Scan

- **Method:** `POST`
- **Path:** `/api/v2/research/astro-scan`
- **Description:** Post Astro Scan

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/research/astro-scan', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 55. Get Astro Events

- **Method:** `GET`
- **Path:** `/api/v2/research/astro-events`
- **Description:** Get Astro Events

### Request Example

`?start_time=value&end_time=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/research/astro-events' + '?start_time=value&end_time=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 56. Get Event Frequency

- **Method:** `GET`
- **Path:** `/api/v2/research/event-frequency`
- **Description:** Get Event Frequency

### Request Example

`?start_time=value&end_time=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/research/event-frequency' + '?start_time=value&end_time=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 57. Get Astro Dataset

- **Method:** `GET`
- **Path:** `/api/v2/research/astro-dataset`
- **Description:** Get Astro Dataset

### Request Example

`?start_time=value`

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/research/astro-dataset' + '?start_time=value');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 58. List all alert rules

- **Method:** `GET`
- **Path:** `/api/v2/alerts/rules`
- **Description:** List all alert rules

### Request Example

No parameters required

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/alerts/rules');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 59. Create a new alert rule

- **Method:** `POST`
- **Path:** `/api/v2/alerts/rules`
- **Description:** Create a new alert rule

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/alerts/rules', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 60. Run manual scan for triggers

- **Method:** `POST`
- **Path:** `/api/v2/alerts/scan`
- **Description:** Run manual scan for triggers

### Request Example

```json
{
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
}
```

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextResponse } from 'next/server';


export async function POST() {

  const payload = {
  "time": {"time": "2024-04-08T18:00:00Z"},
  "location": {"latitude": 40.71, "longitude": -74.00}
};

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/api/v2/alerts/scan', {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify(payload)

  });

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 61. Root

- **Method:** `GET`
- **Path:** `/`
- **Description:** Root

### Request Example

No parameters required

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---

## 62. Version

- **Method:** `GET`
- **Path:** `/version`
- **Description:** Version

### Request Example

No parameters required

### Response Example

```json
{
  "meta": {
    "version": "2.0.0"
  },
  "data": {
    // Extracted target response object 
  }
}
```

### Next.js Usage Example

```typescript
import { NextRequest, NextResponse} from 'next/server';


export async function GET() {

  const res = await fetch(process.env.NEXT_PUBLIC_ASTRO_API_URL + '/version');

  if (!res.ok) throw new Error('API Error');

  const data = await res.json();

  return NextResponse.json(data);

}
```

---
