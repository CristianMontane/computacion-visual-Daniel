export default function ModelInfoPanel({ format, verticesCount }) {
  return (
    <div style={{
      position: 'absolute', top: 10, left: 10, background: '#fff',
      padding: '10px', borderRadius: '8px', fontFamily: 'sans-serif'
    }}>
      <p><strong>Formato:</strong> {format}</p>
      <p><strong>Vértices:</strong> {verticesCount}</p>
    </div>
  );
}
